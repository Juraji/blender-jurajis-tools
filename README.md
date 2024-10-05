# Juraji's Blender Tools

A Blender Add-On which adds some tools that I personally use a lot.  
_And with I, I mean [Juraji](https://github.com/Juraji) :D._

## Why?

I use other applications to pose/style figures for 3D printing. However, these are optimized for 3D renders, not for
printing, so I import them into blender to prepare the model for printing.  
I started using plain Python scripts to automate some of the tasks I use often in my workflow.  
This soon turned into a plethora of scripts, after which I decided it would be nice to have them inside the Blender UI,
with inputs, buttons etc.

## What does it do?

It adds a new panel (Juraji's Tools) to the 3D view of blender and exposes actions that I had scripted before.  
Below are the descriptions for each of the panels/actions.

### Auto Decimate

This panel executes the Decimate modifier, given the Ratio and the number of repeats on all selected objects.  
The cool part is that, by doing this via a script, it eliminates the initial preview, which would be executed when the
modifier is added via the UI.  
Also, I found that decimating at 0.25 would take quite a bit longer then decimating twice at 0.5. Hence, I've added the
repeat option.

### Voxel Remesh

It does exactly what you think it would do. Given the voxel size, it adds a Remesh modifier and applies it to all
selected objects.
Again, via a script it skips the preview step so speeds up the task quite a bit.

### Scale Converter

Probably the most useful option for anyone. It takes the current object scale (say 1/1) and a target scale (e.g. 1/8),
calculates the scale factor and applies it to the selected objects.  
In this example a 200 centimeter tall figure becomes 25 centimeters tall.

### Export

This might be a more specific one. The built-in export options export all or selected objects to a single file.
However, sometimes I create a larger figure which I need to slice into parts and then also export into parts.  
This STL export option will generate a file for each of the selected objects.  
_Note that it takes the current projects location on disk to export the STL files. Make sure you save your project first
or you will get a warning._

## What's next?

I am currently already using this plugin myself, and you are free to do so as well.  
Also, I have a few ideas on how to improve, which are listed below. This is however not a promise, as this is more of a
one-off side project.

On the other hand, if you have any improvements or ideas for additions, please create a ticket/issue, and we'll talk!  
Or maybe you could even help out and create a pull-request. A small note there however, I am quite strict on code-style
and might decline if I deem your addition to be of poor quality or the addition to be out of scope.
Ofcourse, I will always be open for discussion.

### Ideas

* Create preferences for
    * The tab, in which each option appears. Currently, all appear in "Juraji's Tools", which might not be to everyone's
      liking.
    * Preferences for various default values.
* Internationalisation (i18n), if the need arises.
* I also have an idea for "Modifier Templates". I hate the fact that adding a modifier will always calculate a preview
  for the default values. But most times one is going to tweak the values anyway. Having a value template, so modifiers
  spawn with your own defaults would be cool, I think.  
  There is a lot that this idea might require, any ideas? Let me know!

## Links
Some links that you might be interested in, given you are interested in this project:

* Check out my [Printables](https://www.printables.com/@RobinD_690697). I might have that one thing you need and it's free!
* Check out my [Patreon](https://www.patreon.com/moshi_3d_clothing). Specific for DAZ users, clothing and accessories for your 3D figures!
* Check out my [GitHub](https://github.com/Juraji). I share stuff I create in my free time for free!