#include "opencv.hpp"
#include <iostream>

using namespace cv;
using namespace std;
int main() {

VideoCapture videoIn(0);
if (!videoIn.isOpened()) {
    cout << "yo, i ain't see no camera";
    return -1;
}

namedWindow("out", 1);
for (;;) {
    Mat frame;
    videoIn >> frame;
    imshow("out", frame);
    if (waitKey(30) >= 0)
        break;

}
return 1;
}