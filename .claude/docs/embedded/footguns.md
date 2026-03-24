<!-- last_verified: 2026-03-21 -->
# ESP32 Embedded Footguns

## 1. WiFi+BLE Radio Coexistence

**Problem:** ESP32 shares a single 2.4GHz radio between WiFi and BLE. Running both simultaneously causes packet loss on both protocols.

**Details:** ESP-IDF's software coexistence (CONFIG_SW_COEXIST_ENABLE) time-division multiplexes the radio. In practice, expect 20-30% packet loss on each protocol during simultaneous WiFi promiscuous + BLE scanning.

**Mitigation:** For CYT's use case, alternate between WiFi scanning windows and BLE scanning windows rather than running both continuously. Or accept the loss — 70-80% capture rate over 60-second windows is sufficient for persistence detection.

## 2. Promiscuous Mode Channel Limitation

**Problem:** ESP32 can only sniff ONE WiFi channel at a time. Unlike Kismet on Linux with a dedicated monitor-mode adapter, there's no hardware channel scanning.

**Impact:** With 13 channels and 150ms dwell time, a full sweep takes ~2 seconds. You miss packets on other channels during each dwell. Busy environments lose ~60-70% of total packets.

**Mitigation:** For probe request capture, this is acceptable — devices send probes on multiple channels, so you'll catch most devices within a few sweep cycles. Prioritize channels 1, 6, 11 (most common AP channels where devices probe most frequently).

## 3. PSRAM Allocation Gotcha

**Problem:** `malloc()` does NOT automatically use PSRAM even when present. Regular malloc only uses internal SRAM (~320KB usable).

**Fix:** Use `heap_caps_malloc(size, MALLOC_CAP_SPIRAM)` for large allocations. Or set `CONFIG_SPIRAM_USE_MALLOC=y` in menuconfig to make malloc() try PSRAM after SRAM is full (but this adds overhead).

## 4. PSRAM Speed vs SRAM

**Problem:** PSRAM access is ~5-10x slower than internal SRAM (SPI bus vs direct). Tight loops iterating over PSRAM data structures are noticeably slower.

**Mitigation:** Keep hot data (current packet callback state, hash table index) in SRAM. Put bulk storage (device record array, log buffers) in PSRAM. Never access PSRAM from an ISR.

## 5. Flash Wear from Frequent Writes

**Problem:** ESP32 flash has ~10,000-100,000 write cycles per sector (depending on flash chip). Writing device records every 60 seconds will kill flash in months.

**Fix:** Buffer writes in RAM, flush to flash/LittleFS only every 5-10 minutes. Use SD card for high-frequency logging. NVS has built-in wear leveling but is for small key-value data only.

## 6. Promiscuous Callback Runs in WiFi Task Context

**Problem:** The `wifi_sniffer_cb` callback executes in the WiFi driver's task context, NOT your application task. You CANNOT do heavy processing, memory allocation, or blocking operations inside it.

**Fix:** Copy minimal data (MAC, SSID, RSSI, timestamp) into a FreeRTOS queue from the callback. Process the queue in a separate analysis task.

```c
// In callback — fast, no blocking
xQueueSendFromISR(packet_queue, &packet_info, &xHigherPriorityTaskWoken);

// In analysis task — can do heavy work
xQueueReceive(packet_queue, &packet_info, portMAX_DELAY);
process_device_appearance(&packet_info);
```

## 7. No 5GHz on ANY ESP32 Variant

**Problem:** No ESP32 chip supports 5GHz WiFi. The ESP32-C6's "WiFi 6" is 802.11ax but still 2.4GHz only. This is a silicon limitation, not firmware.

**Impact:** Modern devices increasingly probe on 5GHz. Estimated 15-30% of probes are 5GHz-only in typical environments. This is an unavoidable gap.

**Mitigation:** Document the limitation. For a multi-radio handheld, consider pairing ESP32 with a separate 5GHz module (e.g., RTL8812AU USB), but this adds significant complexity and power draw.

## 8. BLE MAC Address Rotation (AirTag Detection)

**Problem:** Apple AirTags, Samsung SmartTags, and most BLE trackers rotate their MAC address every 15-60 minutes. You CANNOT track them by MAC like WiFi devices.

**Fix:** Track by payload fingerprint instead. Apple Find My advertisements have a consistent structure: manufacturer-specific data with company ID 0x004C, type byte 0x12. The rotating public key portion changes, but you can track the presence of "a Find My device" persistently nearby. For finer-grained tracking, the payload includes a 2-byte "hint" field that can be used to distinguish between distinct nearby AirTags.

## 9. Stack Overflow in Tasks

**Problem:** ESP32 FreeRTOS tasks have fixed-size stacks (set at creation). WiFi/BLE callbacks can use significant stack space. Default 2048 bytes is often too small.

**Fix:** Give sniffer-related tasks at least 4096 bytes. Analysis tasks with string formatting (for display or SD logging) need 8192+. Enable `CONFIG_FREERTOS_CHECK_STACKOVERFLOW=y` during development.

## 10. Power Draw in Continuous Scanning Mode

**Problem:** WiFi promiscuous mode + BLE scanning + GPS UART + display = ~200-350mA continuous draw at 3.3V. A 2000mAh LiPo lasts ~6-8 hours.

**Mitigation:** Implement duty cycling — scan for 45 seconds, sleep for 15 seconds. Or scan WiFi for 30s, BLE for 15s, sleep for 15s. Display should auto-dim after inactivity. GPS can be sampled every 30-60 seconds instead of continuously.
