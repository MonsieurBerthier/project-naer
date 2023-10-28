<p align="center">
  <img src="https://img.shields.io/badge/Version-v0.8.0-blue.svg" />
  <img src="https://img.shields.io/badge/Panda3D-1.10.13-blue.svg" />
  <img src="https://img.shields.io/badge/Python-3.7-blue.svg" />
  <img src="https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-blue.svg" />
</p>

<p align="center">
  <img src="content\images\github\preview.gif" />
</p>

<img src="content\images\github\logo.png" align="right"/>


Project Naer
============

Have you always wondered how your car will look in this color?
Or with these wheels? Or with this body kit?
Or maybe you spend more time in Need For Speed customizing your car than
playing the actual game? I have something for you!

Project Naer is a simple application which allows to personalize your car.
Here are the elements you can change to customize your car:
- wheels : rim and tyre, color, diameter, width, camber, offset and toe
- car : color, body kits and every individual part composing its body

You can also change the ground on which the car is sitting
among 10 possibilities.

Project Naer is scalable. This means new content can be added without
having to change a single line of code: the new content will be detected
automatically and added to the corresponding menu.


Screenshots
===========

<img src="content\images\github\garage.png"/>
<img src="content\images\github\bodyshop.png"/>
<img src="content\images\github\mainmenu.png"/>
<img src="content\images\github\nissan_rs13.png"/>


Content
=======

Keep in mind that new content will be added bit by bit during the development.

Available cars:
- Nissan 180SX (RS13) : 24 parts to install
- _more soon ..._

Available wheels:
- Japan Racing JR3
- Japan Racing JR7
- _more soon ..._

Available grounds:
- Asphalt
- Cobblestones
- Concrete Tiles
- Concrete (wet)
- Frozen Lake
- Linoleum
- Marble
- Mosaic
- Mud
- Sand


Dependencies
============

The 3D engine used for this project is Panda3D. 
It can be downloaded here: [panda3d.org/download/sdk-1-10-13/](http://www.panda3d.org/download/sdk-1-10-13/)

This projet has been developed with the version `1.10.13` of Panda3D SDK. This is the recommended version of you want to avoid any surprises.

Also, the following Python modules need to be installed:

```bash
pip install typing-extensions
pip install panda3d-gltf
````

The dependency to `panda3d-simplepbr` is already satisfied
because it is included in the package.

More information on `panda3d-simplepbr` can be found here:
[github.com/Moguri/panda3d-simplepbr](https://github.com/Moguri/panda3d-simplepbr)


Configuration
=============

The default resolution is `1920 x 1080`.

If you want to change it, edit the file `config/release.prc`
and search for the parameter named `win-size`.


License
=======

This project is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).
