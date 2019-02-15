
#include <iostream>
#include "affdex-sdk/include/VideoDetector.h"
#include "affdex-sdk/include/AffdexException.h"
#include "affdex-sdk/include/ProcessStatusListener.h"

using namespace affdex;

class MyListener:public ProcessStatusListener
{

	virtual void onProcessingException(AffdexException ex)
	{
		std::cerr << "Error occurred" << ex.getExceptionMessage();
	}


    virtual void onProcessingFinished()
    {
    	std::cout << "video processing is complete" << std::endl;
    }
};


int main(int argc, char** argsv)
{
	//VideoDetector takes parameters: frame rate, max num faces, face configuration
	double processFrameRate = 30;
	unsigned int maxNumFaces = 2; //will vary by video
	FaceDetectorMode faceConfig = FaceDetectorMode::SMALL_FACES;
	VideoDetector detector(processFrameRate, maxNumFaces, faceConfig);

	//path to affdex classifier data files for processing
	std::string classifierPath = "affdex-sdk/data";
	detector.setClassifierPath(classifierPath);

	//set the listener for VideoDetector
	std::shared_ptr<ProcessStatusListener> psl(new MyListener())
	detector.setProcessStatusListener(psl.get());

	//set detector for engagement, valence, attention metrics
	detector.setDetectEngagement(true);
	detector.setDetectValence(true);
	detector.setDetectAttention(true);


	//start the detector
	detector.start();

	//process the video file
	detector.process(argsv[1]);

	//use boost to write to csv

	//stop detector
	detector.stop();

	delete psl;
	return 0;

}