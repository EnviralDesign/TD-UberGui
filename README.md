
# UberGui V4 ( TD 2021.12380 )

<p align="center">
  <img src="gifs/UGV4_header2.gif">
</p>

**UberGui is a lightweight multi-threaded, webRender UI module for [TouchDesigner](https://derivative.ca/) projects.** The aim is to solve the trifecta of challenges building UI's in TouchDesigner often poses: being fast, feature rich, and visually appealing.

Additionally, UberGui is built as a layer of abstraction directly on top of Custom Parameters, so you can use this in existing projects with little to no additional refactoring.

## Fast, Beautiful, with TouchDesigner-centric features.

### Performance
UberGui uses the webRender TOP in TD which runs a separate threaded instance of an embedded chromium browser. You can spawn many UG UI's and each will run independently of the main TouchDesigner TOE. Keeping your UI's from bogging down your real-time projects.

Both real time performance when many parameters are animated AND the speed in which a totally new ui is generated is very fast.

![ubergui performance animated ](gifs/UGV4_animatedPerformance.gif)

![ubergui performance slider](gifs/UGV4_sliderPerformance.gif)

Resting performance is very low, just the cost of the web render TOP. **NOTE:** *You can even disable the "Enable Thread" parameter, when you want to fully shut down the cook times of UG, for example when a certain window is not open, or part of the software not visible.*

![ubergui performance resting](gifs/UGV4_resting-performance.gif)

### Aesthetic
Since UberGui is built on html/css we have a massive array of pre existing tech and styling options to leverage to build out compelling UIs. For this tool, I've exposed many of these css styling variables to TD, through a custom parameter styles page. You can modify/expose as many others as you'd like very easily with the parameter injection find/replace method.

![ubergui colors](gifs/UGV4_colorChanges2.gif)

You can also change the horizontal alignment of several elements from the styles page.

![ubergui colors](gifs/UGV4_additionalStyling.gif)

### Features
UberGui is built to layer directly on top of existing projects that utilize Custom Parameters, and is intended to be a visual and functional extension of that feature set in TouchDesigner.

That said, it does offer many additional ways to manipulate and set numerical values that can speed up workflows and improve the experience greatly. Those features are covered below.

## Using UberGui

### Initial Setup
The fastest way to get going is to just download the Tox file in this repo, and drag it into your project. If you haven't used UberGui before, I suggest cloning the entire repo or downloading a zip file, and opening the **UberGui_V4_Release.toe** file to see how to use it with examples.

### Input Mode

UberGui supports operation via **mouse**, and via **touchscreen**. **Switching is handled automatically** in the background, so you can switch between them seamlessly.

### Page Filtering

UberGui by default is looking for any custom parameter pages on your source object. If you have some custom pages you wish to have visible, and others not - you can use the other page filtering mode in the config page, which will only show pages named with all upper case characters.

![ubergui page filtering](gifs/pageFiltering.png)

### Scroll Speed

If scrolling or touch interactions are too fast or too slow, you can change the speed and acceleration below:

![ubergui scroll speed](gifs/scrollspeed.png)

---

### Adjusting Values via Sliders
You can adjust the value of any type of numerical parameter just dragging left and right. The min/max ranges of the parameter will determine the range. Menu parameters can also be treated like a slider.

![ubergui slider adjustment](gifs/UGV4_sliders1-1.gif)

---

### Manual Entry via Field
**Double clicking** on any field will launch an editable field that you can type values into. Most parameters have this ability, but some do not (*like the Menu parameter*).

![ubergui field entry1](gifs/UGV4_fieldsEntry1.gif)

You may also **tab to next** for quick entry of several values either in a parameter tuple row or simply down the line. Each tab press will launch a field in the next parameter, if it supports a field.

![ubergui tab through](gifs/UGV4_tabThrough.gif)

You can also **left click on any label**, to automatically enter field entry mode for it's parameter (*if supported*).

![ubergui field entry 2](gifs/UGV4_fieldsEntry2.gif)

You can also type in **valid python expressions** (*in TD math is imported by default for us*).
These will not be set to the TD expression mode of the parameter, it will simply be evaluated when set.

![ubergui field entry expr](gifs/UGV4_fieldsEntryExpr.gif)

You are able to **evaluate** expressions using many of the **common measurement units** as well (*the assumed default unit cm*).

![ubergui field entry units](gifs/UGV4_fieldsEntryUnits.gif)

---

### Scroll Wheel
Depending on where your mouse is inside the UI, the scroll wheel will perform one of two functions generally.

When **scrolling inside a parameter** slider on the right half of the UI, it will **adjust the parameter** value in increments ( **ctrl** *and* **shift** *will scale the increments accordingly* )

![ubergui slider scroll](gifs/UGV4_scrollSlider.gif)

When **scrolling on the left side** of the UI, this will **scroll vertically** through your UI if there is a scroll bar.

![ubergui slider scroll down](gifs/UGV4_scrolldown.gif)

---

### Parameter Reset
**Right Clicking** on any parameter label will **reset the value** to it's TD parameter set default.

![right click reset](gifs/UGV4_rightclick_reset.gif)

---

### Auxiliary UI
**Menu and Color parameters** have special auxiliary UI that will launch over top of UberGui to make it easier to choose a value. You'll see the **triple dot icon** to the right when this is the case. (*file and folder parameters use this icon as well, but they simply launch TouchDesigner's built in picker.*)

![ubergui aux ui](gifs/UGV4_aux_ui.gif)

You can take advantage of the tool-tips overlay, if you include a table DAT in the source object, that contains descriptions of each parameter.

![ubergui tooltips](gifs/UGV4_tooltips.gif)

This is also where you'd specify special functionality for certain types of parameters in the third and fourth columns.

![ubergui override config](gifs/Uberguiconfigoverride_dat-e1612474638287.png)

---

### Touch Screen support

Touch Screens are supported as well, switching happens automatically as you use different inputs.

Scrolling is easy, just drag up and down on the left side of UberGui. You can also use the scrollbar in touch screen mode.

![ubergui tooltips](gifs/UGV4_touch_scrolling.gif)

Using a slider is simple, just drag left or right.

![ubergui touch sliders](gifs/UGV4_sliders3.gif)

To reset a parameter tuplet to it's default value(s), just long press on the label.
**NOTE:** *You can change the global delay for long press in the config page of UG.*

![ubergui touch reset fields](gifs/UGV4_tapHoldToReset.gif)

To enter field mode, just quickly tap any field, or tap the parameter name to the left.

![ubergui touch field entry2](gifs/UGV4_fieldEntry_2.gif)

![ubergui touch field entry2](gifs/UGV4_fieldEntry_3.gif)

---

### Other Features

Parameters that have read only enabled, or who's parameter mode is set to expression, export, or bind will show as follows, and not be editable via UberGui with the exception of Bound parameters.

![ubergui read only](https://user-images.githubusercontent.com/10091486/116152339-68097200-a6ab-11eb-8a6f-92f7f2e11b1a.png)

Disabled parameters will simply be excluded from the UI all together.




## Support this work

If you find value in this sort of thing, help me dedicating time to making open source code.

[![Donate](gifs/paypal.png)](https://www.paypal.com/donate?hosted_button_id=RP8EJAHSDTZ86)
[![Donate](gifs/patron2.png)](https://www.patreon.com/EnviralDesign)
