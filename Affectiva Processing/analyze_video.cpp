
#include <iostream>
#include "affdex-sdk/include/VideoDetector.h"
#include "affdex-sdk/include/AffdexException.h"
#include "affdex-sdk/include/ProcessStatusListener.h"
#include "affdex-sdk/include/FaceListener.h"
#include "affdex-sdk/include/ImageListener.h"
#include <unistd.h>
#include <iostream>
#include <fstream>
using namespace affdex;
bool done = false;
std::ofstream outputFile;
std::string filename = "affectiva_data.csv";
bool yes = false;

class FaceList:public FaceListener
{
	void onFaceFound(float timestamp, FaceId faceId){
		//std::cout<<faceId<<" face found!"<<std::endl;
	}
	void onFaceLost(float timestamp, FaceId faceId){
		//std::cout<<timestamp<<" face LOST!"<<std::endl;
	}
};

class ImageList: public ImageListener{
	
	virtual void onImageResults(std::map<FaceId, Face> faces, Frame image) {
		//std::cout<<"result "<<image.getTimestamp()<<std::endl;
		std::map<FaceId, Face>::iterator it;
		if (!yes){
			outputFile <<"Timestamp,Engagement,Attention,Valence,Joy,Sadness,Anger\n";
			yes = true;
		}
		float t = image.getTimestamp();
		for(it = faces.begin(); it!= faces.end(); it++)
		{	

			outputFile << t<<", ";
			outputFile << it->second.emotions.engagement<< ", ";
			outputFile << it->second.expressions.attention<< ", ";
			outputFile << it->second.emotions.valence<< ",";
			outputFile << it->second.emotions.joy<< ",";
			outputFile << it->second.emotions.sadness<< ",";
			outputFile << it->second.emotions.anger<< "\n";
			std::cout<<it->second.appearance.ethnicity<<"\n";
		}	
	}
    
    virtual void onImageCapture(Frame image){
		//std::cout<<"capture "<<image.getTimestamp()<<std::endl;
    }

};

class MyListener:public ProcessStatusListener
{
	virtual void onProcessingException(AffdexException ex)
	{
		std::cerr << "Error occurred" << ex.getExceptionMessage();
	}

    virtual void onProcessingFinished()
    {
    	std::cout << "video processing is complete" << std::endl;
    	done = true;
    }
};

int main(int argc, char** argsv)
{
	//VideoDetector takes parameters: frame rate, max num faces, face configuration
	double processFrameRate = 30;
	unsigned int maxNumFaces = 1; //will vary by video
	FaceDetectorMode faceConfig = FaceDetectorMode::LARGE_FACES;
	VideoDetector detector(processFrameRate, maxNumFaces, faceConfig);

	//path to affdex classifier data files for processing
	std::string classifierPath = "affdex-sdk/data";
	detector.setClassifierPath(classifierPath);

	//set the listener for VideoDetector
	std::shared_ptr<FaceListener> psl(new FaceList());
	detector.setFaceListener(psl.get());
	std::shared_ptr<ProcessStatusListener> ps2(new MyListener());
	detector.setProcessStatusListener(ps2.get());
	std::shared_ptr<ImageListener> ps3(new ImageList());
	detector.setImageListener(ps3.get());	
	//set detector for engagement, valence, attention metrics
	detector.setDetectEngagement(true);
	detector.setDetectValence(true);
	detector.setDetectAttention(true);
	outputFile.open(filename);

	//start the detector
	detector.start();

	//process the video file
	detector.process(argsv[1]);

	//lol where does the processesd data go? 
	//stop detector
	//usleep(1000000000);
	
	while(!done){
	}
	detector.stop();
	//std::cout << psl->getData();

	outputFile.close();
	//delete psl;
	return 0;

}
