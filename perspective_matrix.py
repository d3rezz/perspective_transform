""" Get perspective transform matrix to use with OpenCV warpPerspective.

    Author: Francisco Salgado
"""

import cv2
import numpy as np


def perspective_matrix(image_w, image_h, theta, phi, fov=np.pi/4):
    """
    Compute a perspective transform matrix using the pinhole camera model.
    Assumes the same horizontal and vertical fov angle.
    Args:
        image_w (int): image width
        image_h (int): image_height
        theta (float): angle in radians to rotate around the z-axis in camera frame (rotate image clockwise)
        phi (float): angle in radians to rorate around the xaxis in camera frame (tilt)
        fov (float): field of view in radians of the 
    Returns:
        M (np.array): perspective transform matrix
        new_image_shape (int, int): new dimensions of the image after applying the perspective tranform.
                                    Computed from the fov of the pinhole model
    """

    # Convert the image to the 3D coordinate space by setting the Z coordinate of image pixel to 0
    to_3d = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0], [0, 0, 1]])

    # Set the origin to the image center
    T = np.eye(4)
    T[0, 3] = -image_w/2
    T[1, 3] = -image_h/2
    T[2, 3] = 0

    # Convert to the camera frame
    R = np.eye(4)
    R[:3,:3] = np.array([[-1, 0, 0], [0, -1, 0], [0, 0 ,1]])

    # Rotate image by theta radians around the z-axis the camera frame
    R_theta = np.eye(4)
    R_theta[0, 0] = np.cos(theta)
    R_theta[0, 1] = -np.sin(theta)
    R_theta[1, 0] = np.sin(theta)
    R_theta[1, 1] = np.cos(theta)
    
    # Rotate image by phi radians around the x-axis the camera frame
    R_phi = np.eye(4)
    R_phi[1, 1] = np.cos(phi)
    R_phi[1, 2] = -np.sin(phi)
    R_phi[2, 1] = np.sin(phi)
    R_phi[2, 2] = np.cos(phi)

    # Size of the side of the square containg any possible rotation
    d = np.sqrt(image_w**2 + image_h**2)
    
    # Translate image away from camera along the z-axis in the camera frame by h
    h = d / (2*np.sin(fov/2))
    T2 = np.eye(4)
    T2[2, 3] = -h

    # Pinhole model intrinsics
    n = h - d/2     # focal length in pixels. Image pane will be placed as close to the image as possible, while still allowing any rotation without cropping.
    new_image_shape = (int(n*np.tan(fov/2)*2), int(n*np.tan(fov/2)*2))  #assumes save horizontal and vertical fov
    K = np.zeros((3,4))
    K[:3,:3] = np.eye(3)
    K[0,0] = n
    K[1,1] = n
    K[0,2] = new_image_shape[0]/2
    K[1,2] = new_image_shape[1]/2
    K[2,3] = 1
  
    # Perspetive matrix
    M = np.matmul(K, np.matmul(T2, np.matmul(R_theta, np.matmul(R_phi, np.matmul(R, T)))))
    M = np.matmul(M, to_3d)

    return M, new_image_shape


if __name__ == "__main__":
    im = cv2.imread("bmw.jpg")
    cv2.imshow("original", im)
    M, new_im_shape = perspective_matrix(im.shape[1], im.shape[0], np.pi/6, np.pi/6, np.pi/4)

    transformed = cv2.warpPerspective(im, M, new_im_shape)

    cv2.imshow("transformed", transformed)
    cv2.waitKey(0)

    cv2.imwrite("transformed.jpg", transformed) 
