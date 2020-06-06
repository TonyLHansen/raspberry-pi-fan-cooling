# Use of Fritzing For Schematic

When I went to creating a Fritzing schematic for this project,
I searched around for a fan component to use.
There were two choices readily available:
* use a generic motor, or
* use the fan created by Karla L Hdz, typical of fans used in desktop computers and found at <https://forum.fritzing.org/t/fan-ventilador-5v-download-piece/2096>.

Unfortunately, I *really* wanted a _small_ fan for my schematic.
(After all, this project was designed around small fans.)

First I tried to figure out how to make fan-ventilador scalable,
which would allow it to be used for schematics with fans of any size.
However, I wasn't too luck with the parts editor.
So, I dove into the internals of the fzpz format and found that I could easily
change the size of the image specified in the svg files.
I also updated the size of the image in the icon, to make it visually different from
that used by fan-ventilador.
I then updated the IDs used in the files to make the new part unique.
The new Fritzing part for a small fan can be found in [small_fan.fzpz](Small_Fan.fzpz).
