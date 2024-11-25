# Taiwanese Voice Ticketing System
An automatic subway ticketing machine that can be controlled by voice.

## Table of Content
- [Installation](#installation)
- [Motivation](#motivation)
- [Architecture](#architecture)
  - [Automated Detection Technology](#automatic-detection-technology)
  - [Independent Space](#independent-space)
  - [Visual Design](#visual-design)
- [Feature](#feature)
- [Prototype](#prototype)
- [Web Design](#web-design)
- [Voice User Interfaces（VUI）](#voice-user-interfaces-vui)
- [Hardware Device](#hardware-device)
- [Installation Locations](#installation-locations)
- [Future Work](#future-work)
- [Demo](#demo)

## Installation
```
python app.py
```

## Motivation
When Taiwanese-speaking users purchase tickets at the counter, they encounter the following problems:

1. Counter staff cannot speak Taiwanese, making the ticket purchase process difficult (communication barrier)
2. Long queues at counters can be reduced by automatic ticket machines

Therefore, we have carefully designed this machine to help elderly people who primarily communicate in Taiwanese and have low technological literacy to purchase tickets using Taiwanese voice commands. Users only need to speak in Taiwanese to purchase same-day tickets, and the system includes options for various train types and ticket types.

Furthermore, to make Taiwanese users feel more comfortable during the experience, we have carefully considered the machine's response terminology, using simple and familiar everyday phrases as responses to reduce anxiety among elderly people during ticket purchases.

## Architecture
### Automatic Detection Technology
This ticketing machine is equipped with a front-facing sensor camera. When it detects a person, it immediately initiates a series of ticket purchase inquiries. To complete or interrupt the purchase at any time, users only need to leave the ticketing area, and when the camera no longer detects a person, it automatically returns to the ticket purchase homepage.

### Independent Space
Due to the noisy environment of train stations, voice recording can be affected. Therefore, we have specially designed an independent small space using sound-insulating materials for the partitions. Additionally, considering that enclosed spaces might cause anxiety among elderly people, the partitions are made of transparent materials that allow visibility to the outside, as shown in the diagram.

![](https://i.imgur.com/vsueeeH.png)

Note: In recent years, Taiwan Railways has been actively promoting its corporate image. The exterior of the independent space can be decorated with wallpapers or eye-catching promotional materials to increase exposure, improve passengers' impression of Taiwan Railways, and enhance international image through media promotion.

### Visual Design
The website's color scheme references Taiwan Railways' deep blue, with bright orange used to emphasize clickable buttons. The illustrations incorporate Taiwan's nationally protected animal — the Formosan Black Bear — as a mascot. The overall interface presents a design that features clean lines, rich illustrations, comfortable color schemes, friendly dialogue, and appropriate font sizes.

![](https://i.imgur.com/rKpv9HK.png)


## Feature
![](https://i.imgur.com/Tm5NR2B.png)

The ticketing machine includes functions as shown in the diagram. Train schedules can be searched by time and train type. The search method uses a selenium web scraper to crawl the Taiwan Railway Timetable.[Taiwan Railway Web](https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/gobytime)

![image](https://user-images.githubusercontent.com/46195804/173881352-8bfc9da1-25e1-4919-a7e8-38d08d09b258.png)

- **Search Nearest Train**
The web scraper recommends the nearest train based on the user's specified time.

- **Search Specific Time/Train Number**
The web scraper recommends the top 3 trains that best match the user's specified train number/time, sorted by fastest arrival time.

Considering that the user group includes elderly people, this machine does not sell tickets for trains departing within 30 minutes. If a user fails to find a preferred train schedule after three consecutive attempts, remote counter service staff assistance will be activated. Similarly, if a user gets stuck at the same step three times during the purchase process, remote human service connection will be triggered.

## Prototype
webpage interface presentation style.

![](https://i.imgur.com/9lGCovO.png)

## Web Design
![](https://i.imgur.com/QhIa3wb.png)

![](https://i.imgur.com/IqMVPJR.png)

## Voice User Interfaces (VUI)
The voice terminology is separated from the displayed text. This is because our target Taiwanese-speaking users are accustomed to reading Chinese text while listening to Taiwanese audio.

![](https://i.imgur.com/PKf1ZIx.png)

## Hardware Device
Existing automatic ticketing machine hardware is rather cluttered. For example, ticket output and change dispensing are separated into different modules. Therefore, we have redesigned the machine with a minimalist design style.

Starting from the rightmost section, there is the cash payment area, including slots for bills and coins.
The middle section is for other payment methods, including credit card insertion slot, credit card tap area, and electronic payment sensing area.
The leftmost section is the ticket area, including ticket collection and refund.
Finally, the bottom section is unified as the output area, including tickets, receipts, and cash dispensing.

![](https://i.imgur.com/Zk6eMIi.png)

## Installation Locations
Currently, this voice machine handles Taiwan Railways ticket purchasing functions, but its functionality could be extended to different areas in the future, such as:

- Post offices/banks
- Movie theaters
- Parking lots


## Future Work
1. Automatically adjust detection camera according to person's heigth.
2. Purchasing boxed meals and consecutive seats judgment
3. Multilingual dialogue
4. Large hardkey buttons, blue for confirmation, red for negation
5. Finding the nearest train station through location
6. Include arrival times, pages can be displayed separately (select one departure, show one arrival)
7. Train number recommendation rules need to reference Taiwan Railways internal SOP process (important)

## Demo
[Taiwan Railways Voice Ticketing Machine Demo Video](https://youtu.be/b_ZXO2HMm64)
