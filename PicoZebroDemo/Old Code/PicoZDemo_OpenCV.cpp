#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "RaspiCamCV.h"

int main(int argc, char** argv) {
  RaspiCamCvCapture * camera = raspiCamCvCreateCameraCapture(0);
  cv::Mat image(raspiCamCvQueryFrame(camera));
  cv::namedWindow("Display", CV_WINDOW_AUTOSIZE);
  cv::imshow(window_name, image);
  cv::waitKey(0);
  return 0;
}
