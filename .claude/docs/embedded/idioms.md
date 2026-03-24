<!-- last_verified: 2026-03-21 -->
# ESP32 Embedded Idioms

## WiFi Promiscuous Mode (ESP-IDF v5.x)

### Basic probe request capture
```c
// Register callback before enabling promiscuous mode
esp_wifi_set_promiscuous_rx_cb(wifi_sniffer_cb);
esp_wifi_set_promiscuous(true);

// Filter to management frames only (probe requests are subtype 0x04)
wifi_promiscuous_filter_t filter = {
    .filter_mask = WIFI_PROMIS_FILTER_MASK_MGMT
};
esp_wifi_set_promiscuous_filter(&filter);
```

### Packet callback pattern
```c
void wifi_sniffer_cb(void *buf, wifi_promiscuous_pkt_type_t type) {
    if (type != WIFI_PKT_MGMT) return;

    wifi_promiscuous_pkt_t *pkt = (wifi_promiscuous_pkt_t *)buf;
    wifi_pkt_rx_ctrl_t ctrl = pkt->rx_ctrl;

    // RSSI is in ctrl.rssi (signed int8)
    // Channel is in ctrl.channel
    // Raw frame starts at pkt->payload
    // Frame subtype is in payload[0] — probe request = 0x40

    uint8_t frame_subtype = pkt->payload[0] & 0xF0;
    if (frame_subtype != 0x40) return; // Not a probe request

    // Source MAC is at offset 10 (bytes 10-15)
    uint8_t *src_mac = &pkt->payload[10];

    // SSID is in the tagged parameters starting at offset 24
    // Tag 0 = SSID, length at offset 25, SSID string at offset 26
}
```

### Channel hopping
```c
// Hop through 2.4GHz channels (1-13, or 1-11 for US)
void channel_hop_task(void *pvParameters) {
    uint8_t channel = 1;
    while (1) {
        esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE);
        vTaskDelay(pdMS_TO_TICKS(150)); // 150ms dwell per channel
        channel = (channel % 13) + 1;
    }
}
```

## FreeRTOS Task Pinning (Dual-Core)

```c
// Pin WiFi sniffer to Core 0, analysis to Core 1
xTaskCreatePinnedToCore(wifi_sniffer_task, "sniffer", 4096, NULL, 5, NULL, 0);
xTaskCreatePinnedToCore(analysis_task, "analysis", 8192, NULL, 3, NULL, 1);
```

## PSRAM Usage (ESP32-S3 with PSRAM)

```c
// Allocate large buffers in PSRAM, not SRAM
device_table = (device_record_t *)heap_caps_malloc(
    MAX_DEVICES * sizeof(device_record_t),
    MALLOC_CAP_SPIRAM
);

// Check allocation succeeded (PSRAM may not be present)
if (device_table == NULL) {
    ESP_LOGE(TAG, "PSRAM allocation failed — reduce MAX_DEVICES");
}
```

## Binary Device Record (Memory-Efficient)

```c
// Fixed-size record for device tracking (~48 bytes vs ~200+ in Python)
typedef struct {
    uint8_t  mac[6];           // 6 bytes
    uint8_t  ssid[33];         // 33 bytes (32 chars + null)
    uint8_t  ssid_len;         // 1 byte
    int8_t   rssi_avg;         // 1 byte
    uint8_t  appearance_count; // 1 byte (max 255)
    uint8_t  window_flags;     // 1 byte (bitfield: seen in 5/10/15/20 min windows)
    uint32_t first_seen;       // 4 bytes (epoch seconds)
    uint32_t last_seen;        // 4 bytes
} __attribute__((packed)) device_record_t;
```

## GPS via UART (u-blox NEO-6M/M8N)

```c
// Configure UART for GPS NMEA at 9600 baud
uart_config_t uart_config = {
    .baud_rate = 9600,
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_1,
};
uart_param_config(UART_NUM_1, &uart_config);
uart_set_pin(UART_NUM_1, GPS_TX_PIN, GPS_RX_PIN, -1, -1);

// Parse NMEA $GPRMC or $GPGGA sentences for lat/lon
```

## BLE Advertisement Scanning

```c
// Start BLE scan for tracker detection
esp_ble_gap_set_scan_params(&scan_params);
esp_ble_gap_start_scanning(0); // 0 = continuous

// In GAP callback, filter for tracker manufacturer IDs
void gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param) {
    if (event == ESP_GAP_BLE_SCAN_RESULT_EVT) {
        // Check manufacturer-specific data for:
        // Apple Find My: company_id 0x004C, type 0x12
        // Samsung SmartTag: company_id 0x0075
        // Tile: service UUID 0xFFFE
    }
}
```

## SD Card Logging (SPI Mode)

```c
// Mount SD card via SPI
sdmmc_host_t host = SDSPI_HOST_DEFAULT();
sdspi_device_config_t slot_config = SDSPI_DEVICE_CONFIG_DEFAULT();
slot_config.gpio_cs = PIN_NUM_CS;

esp_vfs_fat_sdspi_mount("/sdcard", &host, &slot_config, &mount_config, &card);

// Write CSV records for PC post-processing
FILE *f = fopen("/sdcard/cyt_log.csv", "a");
fprintf(f, "%02X:%02X:%02X:%02X:%02X:%02X,%s,%d,%lu\n",
        mac[0], mac[1], mac[2], mac[3], mac[4], mac[5],
        ssid, rssi, (unsigned long)timestamp);
fclose(f);
```

## Display Update Pattern (ST7789 TFT via SPI)

```c
// Use LVGL or direct SPI writes
// Update display from analysis task, not sniffer task
// Typical refresh: every 1-2 seconds, not per-packet
void update_display(analysis_results_t *results) {
    tft_fill_rect(0, 0, 240, 135, TFT_BLACK);
    tft_draw_string(0, 0, "CYT-ESP32", TFT_WHITE);
    tft_draw_string(0, 16, buf_devices, TFT_GREEN);

    if (results->alert_count > 0) {
        tft_draw_string(0, 48, "!! ALERT !!", TFT_RED);
    }
}
```
