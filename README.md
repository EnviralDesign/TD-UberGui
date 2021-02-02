
# UberGui
UberGui is a lightweight multi-threaded, webRender UI module for TouchDesigner projects.

The aim is to solve the trifecta of challenges building UI's in TouchDesigner often poses: being fast, feature rich, and visually appealing.

Additionally, UberGui is built as a layer of abstraction directly on top of Custom Parameters, so you can use this in existing projects with little to no additional refactoring.

---
UberGui handles those issues in the following ways:

 - **Speed** - UberGui uses the webRender TOP in TD which runs a separate threaded instance of an embedded chromium browser. You can spawn many UI's and each will run independently of the main TouchDesigner TOE.

 -  **Aesthetic** - Since UberGui is built on html/css we have a massive array of pre existing tech and styling options to leverage to build out compelling UIs. For this tool, I've exposed many of these css styling variables to TD, through a custom parameter styles page. You can modify/expose as many others as you'd like very easily with the parameter injection find/replace method.

 - **Features** - UberGui is built to layer directly on top of existing projects that utilize Custom Parameters. That said, it does offer many additional ways to manipulate and set numerical values that can speed up workflows and improve the experience greatly. Those features are covered below.

---
