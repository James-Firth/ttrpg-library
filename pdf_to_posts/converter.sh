#!/bin/bash

convert image.pdf[0-7] -thumbnail 140x140 -background white +smush 20 -bordercolor white -border 10 result.jpg
