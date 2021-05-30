# ark_auto
Auto run Arknights stages on your android phone

You need to connect your phone to your computer and have debug mode enabled

## Prerequisite
Download google adb tools at:
https://developer.android.com/studio/releases/platform-tools

extract the zip file and add the folder containing adb.exe into you path environment.

Run ```adb --version``` to make sure you have adb configured properly.
## Arguments
```
-n Specify number of runs

-c Specify the cost of the stage
-s Specify your current sanity

```


## Settings
config the following parameters in the ``` 'config.ini'``` file:

```start_button_0```  XXX YYY cor of the start op button in the stage selecting screen

```start_button_1```  XXX YYY cor of the start op button in the operator selecting screen

```detect_point```  XXX YYY cor of the vertical white line at the stage finishing screen. Any point on the line should work.

```white_value``` Usually you don't want to change this, but if you enconter difficultiy at detecting a run is finished, you may want to lower this value.

