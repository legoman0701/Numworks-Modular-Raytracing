# Numworks-Modular-Raytracing
My first modular Ray tracing engine made for numworks calculator

##### <h2>Table of Contents</h2>
[Credit](#credit)  

[Blender Support](#blender-support)  

[Template to add object manually](#template-to-add-object-manually) 

[Somes images](#somes-images)  

[For The futur](#for-the-futur)  



<a name="credit"/>
<h1>Credit:</h1>

Huge thanks to **Sebastian Lague**
https://www.youtube.com/watch?v=Qz0KTGYJtUk&t=1418s

to **cs.princeton.edu**
https://www.cs.princeton.edu/courses/archive/fall00/cs426/lectures/raycast/sld017.htm

to **antonako** and **idmean**
https://stackoverflow.com/a/6178290

and to **Ray Tracing in One Weekend**
https://raytracing.github.io

<h1>Blender Support</h1>
To convert a blender scene into the raytracer I made a python script (its bad).

First to optimize the rendering engine if the object has `sphere` in its name is will be considered as a sphere with a fixed radius and nothing else

And if it has `plane` it will be considered as an infinite plane and nothing else

Next all the meshes in your scene need to be tris not quad to convert them you can use the triangulate modifier:
First add the modifier the object

![image](https://github.com/legoman0701/Numworks-Modular-Raytracing/blob/main/image/Triangulate.png)

Then apply it

![image](https://github.com/legoman0701/Numworks-Modular-Raytracing/blob/main/image/Apply_triangulate.png)

Next, you need to select all the object in the scene and then run the script

![image](https://github.com/legoman0701/Numworks-Modular-Raytracing/blob/main/image/Run_script.png)

The output of the script will be in a file named ‘scene.txt’.

![image](https://github.com/legoman0701/Numworks-Modular-Raytracing/blob/main/image/Output.png)

Just copy the content of the file in the appropriate part of the code

<h1>Template to add object manually</h1>


mesh

    {

        'type': 'mesh',
        'mesh': mesh,
        'position': (-0.91, -5.46, 22.11),
        'color': (1, 1, 1),
        'metallic': 0,
        'roughness': 1,
        'specular': 0,
        'emmisiveColor': (1, 1, 1),
        'emmisiveStrenght': 0
    },


sphere

    {
        'type': 'sphere',
        'position': (-1, 0, -7),
        'radius': 1,
        'color': (0, 1, 0),
        'metallic': 0,
        'roughness': 1,
        'specular': 0,
        'emmisiveColor': (1, 1, 1),
        'emmisiveStrenght': 0
    },


plane

    {
        'type': 'plane',
        'position': (0, -5.46001, 0),
        'normal': (0, 1, 0),
        'size': 5,
        'color': (1, 1, 1),
        'metallic': 0,
        'roughness': 1,
        'specular': 0,
        'emmisiveColor': (1, 1, 1),
        'emmisiveStrenght': 0
    },


<h1>Somes images</h1>

pc-11m 43s numworks n110 ~32h 10m 19s

![image](https://github.com/legoman0701/Numworks-Modular-Raytracing/blob/main/image/render%2011m%2043s.png)

pc-5m 12s numworks n110 ~12h 43m 6s

![image](https://github.com/legoman0701/Numworks-Modular-Raytracing/blob/main/image/render%205m%2012s.png)

pc-30m 15s numworks n110 ~3j 1h 59m 11s

![image](https://github.com/legoman0701/Numworks-Modular-Raytracing/blob/main/image/render%2030m%2015s.png)

![image](https://github.com/legoman0701/Numworks-Modular-Raytracing/blob/main/image/evo.gif)

The numworks n110 take roughly 146,75 the time of my computer

<h1>For The futur</h1>

For the future of this project, I would like to add glass support and fix the glitches with the mesh and planes

Some’s optimization

And convert this code to C++ to make it into a Numworks app to run faster but i dont C how to do it (sorry)

(Sorry for bad English)
