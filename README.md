# Manually Computing a Perspective Transformation Matrix
Python function to manually compute a perspective transform matrix from the given rotations <img src="https://latex.codecogs.com/svg.latex?%5Ctheta"/> (around the z-axis) and <img src="https://latex.codecogs.com/svg.latex?%5Cphi"/> (around the x-axis) in the camera frame.

The resulting 3x3 transform matrix can then be plugged into OpenCV and Tensorflow using `cv2.warpPerspective` and `tf.contrib.image.transform`.

<div align="center">
    <table align="center">
	    <tr>
            <td style="padding:5px">
        	    <img src="bmw.jpg" height="250" />
      	    </td>
            <td style="padding:5px">
        	    <img src="transformed.jpg" height="250" />
      	    </td> 
        </tr>
        <tr>
            <td align="center" style="border-top: none">Original</td>
            <td align="center" style="border-top: none">Transformed</td>
        </tr>
    </table>
</div>


The code on this repository was inspired by this [post](https://stackoverflow.com/questions/17087446/how-to-calculate-perspective-transform-for-opencv-from-rotation-angles%22%22%22) on Stack Overflow.

## How it works
The perspective matrix is computed using the pinhole camera model:

<div align="center">
	<img src="https://latex.codecogs.com/svg.latex?s%20%5Cbegin%7Bbmatrix%7D%20u%5C%5C%20v%5C%5C%201%20%5Cend%7Bbmatrix%7D%20%3DK%20%5Cbegin%7Bbmatrix%7D%20r_%7B11%7D%20%26%20r_%7B12%7D%20%26%20r_%7B13%7D%20%26%20t_%7B1%7D%5C%5C%20r_%7B21%7D%20%26%20r_%7B22%7D%20%26%20r_%7B23%7D%20%26%20t_%7B2%7D%5C%5C%20r_%7B31%7D%20%26%20r_%7B32%7D%20%26%20r_%7B33%7D%20%26%20t_%7B3%7D%20%5Cend%7Bbmatrix%7D%20%5Cbegin%7Bbmatrix%7D%20X%5C%5C%20Y%5C%5C%20Z%5C%5C%201%20%5Cend%7Bbmatrix%7D"/>
</div>

It assumes the same horizontal and vertical field of view for the camera model, which results in a square image.

The coordinates of the image are first converted to the camera frame. Both <img src="https://latex.codecogs.com/svg.latex?%5Ctheta"/> and <img src="https://latex.codecogs.com/svg.latex?%5Cphi"/> rotations are then applied in the camera frame. Lastly, the image pane is set as close to the image as possible while still allowing room for any image rotation.

For more details, refer to my code implementation and to the Stack Overflow post linked above.