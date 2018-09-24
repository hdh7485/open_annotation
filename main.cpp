#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char** argv )
{
    Mat image;
	Mat grayImage;
	Mat blurImage;
	Mat cannyImage;
	Mat contourImage;
	Mat resultImage;

	RNG rng(12345);

	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;

    if ( argc != 2 ){
		image = imread( "narrow_path_1.jpg", 1 );
    }
	else{
		image = imread( argv[1], 1 );
	}

    if ( !image.data )
    {
        printf("No image data \n");
        return -1;
    }

	bilateralFilter(image, blurImage, 3, 75, 75);
	cvtColor(blurImage, grayImage, CV_BGR2GRAY);
	Canny(grayImage, cannyImage, 150, 250, 3);
	
	findContours(cannyImage, contours, hierarchy, RETR_TREE, CHAIN_APPROX_SIMPLE);

    Mat drawing = Mat::zeros( cannyImage.size(), CV_8UC3 );
    for( size_t i = 0; i< contours.size(); i++ )
    {
        Scalar color = Scalar( rng.uniform(0, 256), rng.uniform(0,256), rng.uniform(0,256) );
        drawContours( drawing, contours, (int)i, color, 2, LINE_8, hierarchy, 0 );
    }


    namedWindow("Display Image", WINDOW_AUTOSIZE );
    imshow("Display Image", image);
    namedWindow("Blur Image", WINDOW_AUTOSIZE );
    imshow("Blur Image", blurImage);
    namedWindow("Canny Image", WINDOW_AUTOSIZE );
    imshow("Canny Image", cannyImage);
    namedWindow("Contour Image", WINDOW_AUTOSIZE );
    imshow("Contour Image", drawing);

    waitKey(0);

    return 0;
}
