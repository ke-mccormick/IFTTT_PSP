# IFTTT_PSP
Application activates IFTTT web triggers based on Power Smart Pricing electrical rate. 

https://www.powersmartpricing.org/

The purpose of this program is to activate a IFTTT web trigger if the PSP price is greater than a user defined pricing point, and will activate a different IFTTT web trigger when the price is equal or less than the user defined pricing point.

The program requires IFTTT webhooks called PSP_Price_High_Notify and PSP_Price_Low_Notify for one time notifications when price level changes. The program requires IFTTT webhooks called PSP_Price_High and PSP_Price_Low for activating triggers every hour based on the pricing level. Make sure the webhook event names match the names listed above and configure the applets however you like be notified.

https://ifttt.com/

IFTTT can be slow, so do not expect notification right away. I have asked Power Smart Pricing to integrate with IFTTT, but that has not happened yet. When Power Smart Pricing integrates with IFTTT this application would be unnecessary.

You could use IFTTT to control the Ecobee thermostat, but this can take 30 minutes for the thermostat to update after trigger. Alternatively if you have an Ecobee thermostat, the Ecobee API updates happens nearly instantly after triggering. Please see the Ecobee_PSP application.

**Notice: The file IFTTT_id.txt is only an example and contain bogas data. The file will not work, please read below on how to configure them.

IFTTT_id.txt contains the key hash for the webhooks and can be found in Maker Webhooks settings.

You will need to get the information contained in the files from IFTTT for your specific installation.

This application also requires the use of CURL, so be sure to have CURL installed.

https://curl.haxx.se/

All files need to be in same directory.

Usage: psp.py -n -p price

-n		Optional: Enables IFTTT notification.

-p price	Required: Defines the maximum Power Smart Pricing price.

Example: psp.py -n -p 4.3

If you do not want IFTTT one time transition notifications then leave off the -n parameter.

Max Price is the Maximum Power Smart Pricing price per kWh you are willing to pay with HVAC system running normally.

If the price becomes higher than the Max Price your thermostat will be put in away mode, reducing run time until the Power Smart Pricing price is reduced to or less than the Max Price.

You may use the Ameren Electric Supply price or whatever price you prefer.

https://www.pluginillinois.org/FixedRateBreakdownAmeren.aspx
