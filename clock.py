import SSD1331
import datetime
import time
import math
import serial

SSD1331_PIN_CS  = 8
SSD1331_PIN_DC  = 5
SSD1331_PIN_RST = 25
SSD1331_MAX_WIDTH  = 0x60
SSD1331_MAX_HEIGHT = 0x40

if __name__ == '__main__':
    device = SSD1331.SSD1331(SSD1331_PIN_DC, SSD1331_PIN_RST, SSD1331_PIN_CS)
    try:
        device.EnableDisplay(True)
        device.Clear()
        clock_ticks = []
        for i in range(12):
            hours_angle = 270 + (30 * i)
            clock_ticks.append([])
            clock_ticks[i].append(int(math.cos(math.radians(hours_angle)) * 19))
            clock_ticks[i].append(int(math.sin(math.radians(hours_angle)) * 19))
            clock_ticks[i].append(int(math.cos(math.radians(hours_angle)) * 21))
            clock_ticks[i].append(int(math.sin(math.radians(hours_angle)) * 21))
            
        today_last_time = "Unknown"
        while True:
            my_now = datetime.datetime.now()
            today_date = my_now.strftime("%d.%m.%y")
            today_time = my_now.strftime("%H:%M:%S")
            if today_time != today_last_time:
                hours_angle = 270 + (30 * (my_now.hour + (my_now.minute / 60.0)))
                hours_dx = int(math.cos(math.radians(hours_angle)) * 12)
                hours_dy = int(math.sin(math.radians(hours_angle)) * 12)
                minutes_angle = 270 + (6 * my_now.minute)
                minutes_dx = int(math.cos(math.radians(minutes_angle)) * 17)
                minutes_dy = int(math.sin(math.radians(minutes_angle)) * 17)
                seconds_angle = 270 + (6 * my_now.second)
                seconds_dx = int(math.cos(math.radians(seconds_angle)) * 19)
                seconds_dy = int(math.sin(math.radians(seconds_angle)) * 19)
                device.Clear()
                time.sleep(0.005)
                device.DrawCircle(21, 42, 21, SSD1331.COLOR_YELLOW)
                for i in range(12):
                    device.DrawLine(21 + clock_ticks[i][0], 42 + clock_ticks[i][1], 21 + clock_ticks[i][2], 42 + clock_ticks[i][3], SSD1331.COLOR_YELLOW)
                
                device.DrawLine(21, 42, 21 + hours_dx, 42 + hours_dy, SSD1331.COLOR_WHITE)
                device.DrawLine(21, 42, 21 + minutes_dx, 42 + minutes_dy, SSD1331.COLOR_WHITE)
                device.DrawLine(21, 42, 21 + seconds_dx, 42 + seconds_dy, SSD1331.COLOR_RED)
                device.DrawString(46, 29, today_time, SSD1331.COLOR_WHITE)
                device.DrawString(46, 49, today_date, SSD1331.COLOR_GREEN)
                today_last_time = today_time
            time.sleep(0.5)
    finally:
        device.EnableDisplay(True)
        device.Remove()
