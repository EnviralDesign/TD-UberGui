# UberGui V4

<p align="center">
  <img src="https://www.geopix.io/wp-content/uploads/2021/02/UGV4_header2.gif">
</p>

**UberGui is a lightweight multi-threaded, webRender UI module for [TouchDesigner](https://derivative.ca/) projects.** The aim is to solve the trifecta of challenges building UI's in TouchDesigner often poses: being fast, feature rich, and visually appealing.

Additionally, UberGui is built as a layer of abstraction directly on top of Custom Parameters, so you can use this in existing projects with little to no additional refactoring.



## Fast, Beautiful, with TouchDesigner-centric features.

### Speed
UberGui uses the webRender TOP in TD which runs a separate threaded instance of an embedded chromium browser. You can spawn many UI's and each will run independently of the main TouchDesigner TOE. Keeping your UI's from bogging down your real-time projects.

The gif below was captured at 60 fps in TouchDesigner with no dips with a resting cook time of 1ms. Sometimes during interaction with the UI, cumulative cook time can peak to 2 or 3 ms, but rarely higher.

![ubergui speed](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_header2.gif)

### Aesthetic
Since UberGui is built on html/css we have a massive array of pre existing tech and styling options to leverage to build out compelling UIs. For this tool, I've exposed many of these css styling variables to TD, through a custom parameter styles page. You can modify/expose as many others as you'd like very easily with the parameter injection find/replace method.
![ubergui colors](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_colorChanges2.gif)



### Features
UberGui is built to layer directly on top of existing projects that utilize Custom Parameters, and is intended to be a visual and functional extension of that feature set in TouchDesigner.

That said, it does offer many additional ways to manipulate and set numerical values that can speed up workflows and improve the experience greatly. Those features are covered below.

## Using UberGui

### Initial Setup
The fastest way to get going is to just download the Tox file in this repo, and drag it into your project. If you haven't used UberGui before, I suggest cloning the entire repo or downloading a zip file, and opening the **UberGui_V4_Release.toe** file to see how to use it with examples.

### Adjusting Values via Sliders
You can adjust the value of any type of numerical parameter just dragging left and right. The min/max ranges of the parameter will determine the range. Menu parameters can also be treated like a slider.
![ubergui slider adjustment](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_sliders1-1.gif)

### Manual Entry via Field
**Double clicking** on any field will launch an editable field that you can type values into. Most parameters have this ability, but some do not (*like the Menu parameter*).
![ubergui field entry1](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_fieldsEntry1.gif)

You may also **tab to next** for quick entry of several values either in a parameter tuple row or simply down the line. Each tab press will launch a field in the next parameter, if it supports a field.
![ubergui field entry1](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_tabThrough.gif)

You can also **left click on any label**, to automatically enter field entry mode for it's parameter (*if supported*).
![ubergui field entry 2](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_fieldsEntry2.gif)

You can also type in **valid python expressions** (*in TD math is imported by default for us*).
These will not be set to the TD expression mode of the parameter, it will simply be evaluated when set.
![ubergui field entry expr](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_fieldsEntryExpr.gif)

You are able to **evaluate** expressions using many of the **common measurement units** as well (*the assumed default unit cm*).
![ubergui field entry expr](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_fieldsEntryUnits.gif)

### Scroll Wheel
Depending on where your mouse is inside the UI, the scroll wheel will perform one of two functions generally.

When **scrolling inside a parameter** slider on the right half of the UI, it will **adjust the parameter** value in increments ( **ctrl** *and* **shift** *will scale the increments accordingly* )
![ubergui slider scroll](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_scrollSlider.gif)

When **scrolling on the left side** of the UI, this will **scroll vertically** through your UI if there is a scroll bar.
![ubergui slider scroll down](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_scrolldown.gif)

### Parameter Reset
**Right Clicking** on any parameter label will **reset the value** to it's TD parameter set default.
![ubergui slider scroll down](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_rightclick_reset.gif)

### Auxiliary UI
**Menu and Color parameters** have special auxiliary UI that will launch over top of UberGui to make it easier to choose a value. You'll see the **triple dot icon** to the right when this is the case. (*file and folder parameters use this icon as well, but they simply launch TouchDesigner's built in picker.*)
![ubergui aux ui](https://www.geopix.io/wp-content/uploads/2021/02/UGV4_aux_ui.gif)
