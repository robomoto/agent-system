<!-- last_verified: 2026-03-21 -->
# ESP32 Reference

## ESP32 Family Comparison (as of ESP-IDF v5.x)

| Variant | CPU | Clock | SRAM | PSRAM | WiFi | BLE | USB | Notes |
|---------|-----|-------|------|-------|------|-----|-----|-------|
| ESP32 | Dual Xtensa LX6 | 240MHz | 520KB | Up to 4MB | 802.11 b/g/n | BT 4.2 + BLE | No native | Most mature, most community support |
| ESP32-S2 | Single Xtensa LX7 | 240MHz | 320KB | Up to 4MB | 802.11 b/g/n | **None** | USB-OTG | Skip — no BLE |
| ESP32-S3 | Dual Xtensa LX7 | 240MHz | 512KB | Up to 8MB | 802.11 b/g/n | BT 5.0 + BLE | USB-OTG | **Best all-rounder** |
| ESP32-C3 | Single RISC-V | 160MHz | 400KB | None | 802.11 b/g/n | BT 5.0 + BLE | No native | Ultra low cost, minimal |
| ESP32-C6 | Single RISC-V | 160MHz | 512KB | None | **802.11ax** (WiFi 6) | BT 5.3 + BLE | No native | WiFi 6, Thread/Zigbee coprocessor |
| ESP32-H2 | Single RISC-V | 96MHz | 320KB | None | **None** | BT 5.3 + BLE | No native | BLE/Thread/Zigbee only |

## Key ESP-IDF APIs for CYT

### WiFi Promiscuous Mode
```
esp_wifi_set_promiscuous(bool enable)
esp_wifi_set_promiscuous_rx_cb(wifi_promiscuous_cb_t cb)
esp_wifi_set_promiscuous_filter(const wifi_promiscuous_filter_t *filter)
esp_wifi_set_channel(uint8_t primary, wifi_second_chan_t second)
```

### BLE GAP Scanning
```
esp_ble_gap_set_scan_params(esp_ble_scan_params_t *params)
esp_ble_gap_start_scanning(uint32_t duration)  // 0 = continuous
esp_ble_gap_stop_scanning()
// Results delivered via ESP_GAP_BLE_SCAN_RESULT_EVT callback
```

### Storage
```
// NVS (key-value, wear-leveled, for config)
nvs_open(), nvs_set_*(), nvs_get_*(), nvs_commit()

// LittleFS (filesystem, for logs and device records)
esp_vfs_littlefs_register()
// Then use standard fopen/fwrite/fclose

// SD Card (SPI mode)
esp_vfs_fat_sdspi_mount()
// Then use standard fopen/fwrite/fclose at /sdcard/
```

### FreeRTOS Essentials
```
xTaskCreatePinnedToCore()  // Pin task to specific core
xQueueCreate() / xQueueSend() / xQueueReceive()  // Inter-task communication
xSemaphoreCreateMutex()  // Protect shared data
vTaskDelay(pdMS_TO_TICKS(ms))  // Non-blocking delay
```

## Recommended Dev Boards for CYT Handheld

| Board | Chip | Display | GPS | SD | Battery | Price | Notes |
|-------|------|---------|-----|-----|---------|-------|-------|
| LilyGo T-Display-S3 | ESP32-S3 | 1.9" 170x320 TFT | No (add UART) | No (add SPI) | LiPo connector | ~$15 | Best compact option |
| LilyGo T-Display-S3 AMOLED | ESP32-S3 | 1.91" AMOLED | No | No | LiPo connector | ~$20 | Beautiful display |
| TTGO T-Beam v1.2 | ESP32 (original) | 0.96" OLED | **Built-in u-blox** | No | 18650 holder | ~$25 | **Best for GPS** |
| M5Stack Core S3 | ESP32-S3 | 2.0" 320x240 TFT | No | Yes (built-in) | Built-in 500mAh | ~$45 | Most complete, pricey |
| Heltec WiFi Kit 32 V3 | ESP32-S3 | 0.96" OLED | No | No | LiPo connector | ~$12 | Cheapest S3 with display |

## Memory Budget (ESP32-S3 with 8MB PSRAM)

| Component | SRAM Usage | PSRAM Usage |
|-----------|-----------|-------------|
| WiFi stack | ~60KB | — |
| BLE stack | ~40KB | — |
| FreeRTOS + tasks | ~30KB | — |
| Display driver | ~20KB | Frame buffer ~100KB |
| Packet queue (256 entries) | ~16KB | — |
| Hash table index | ~16KB | — |
| Device records (10K devices) | — | ~480KB |
| Log buffer | — | ~64KB |
| GPS NMEA parser | ~4KB | — |
| **Total** | **~186KB** | **~644KB** |
| **Available** | **~334KB free** | **~7.4MB free** |

## 802.11 Probe Request Frame Structure

```
Offset  Size  Field
0       1     Frame Control (subtype 0x04 = Probe Request)
1       1     Flags
2       2     Duration
4       6     Destination MAC (FF:FF:FF:FF:FF:FF for broadcast)
10      6     Source MAC (this is the device's MAC)
16      6     BSSID (FF:FF:FF:FF:FF:FF for wildcard)
22      2     Sequence Control
24      N     Tagged Parameters:
              - Tag 0: SSID (length 0 = wildcard, 1-32 = directed probe)
              - Tag 1: Supported Rates
              - Other tags...
```

## BLE Tracker Advertisement Identification

| Tracker | Company ID | Type Byte | Service UUID | Notes |
|---------|-----------|-----------|--------------|-------|
| Apple AirTag / Find My | 0x004C | 0x12 | — | Rotates MAC every ~15 min |
| Samsung SmartTag | 0x0075 | — | — | SmartThings Find network |
| Tile | — | — | 0xFFFE | Tile service UUID in adv data |
| Chipolo ONE Spot | 0x004C | 0x12 | — | Uses Apple Find My network |
| Google Find My Device | TBD | TBD | TBD | New network, spec evolving |
