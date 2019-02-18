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
bool noprint_header = false;
std::ofstream faceFile;

class FaceList: public FaceListener {
	    virtual void onFaceLost(float timestamp, FaceId faceId){
	    	faceFile<<timestamp<<",FACE LOST \n";
	    }
        virtual void onFaceFound( float timestamp, FaceId faceId ) {
        	faceFile<<timestamp<<",FACE FOUND \n";
        }

};
class ImageList: public ImageListener{

	virtual void onImageResults(std::map<FaceId, Face> faces, Frame image) {
		
		std::map<FaceId, Face>::iterator it;
		if (!noprint_header){
			outputFile <<"Timestamp,Engagement,Attention,Valence,Joy,Sadness,Anger,Fear,Disgust,Surprise,Contempt,Smile,";
			outputFile << "InnerBrowRaise,BrowRaise,BrowFurrow,NoseWrinkle,UpperLipRaise,LipCornerDepressor,ChinRaise,LipPucker,";
			outputFile << "LipPress,LipSuck,MouthOpen,Smirk,EyeClosure,EyeWiden,CheekRaise,LidTighten,Dimpler,LipStretch,JawDrop\n";
			noprint_header = true;
		}
		for(it = faces.begin(); it!= faces.end(); it++)
		{	
			outputFile << image.getTimestamp() << ", ";
			outputFile << it->second.emotions.engagement<< ", ";
			outputFile << it->second.expressions.attention<< ", ";
			outputFile << it->second.emotions.valence<< ",";
			outputFile << it->second.emotions.joy<< ",";
			outputFile << it->second.emotions.sadness<< ",";
			outputFile << it->second.emotions.anger<< ",";
			outputFile << it->second.emotions.fear<< ",";
			outputFile << it->second.emotions.disgust<< ",";
			outputFile << it->second.emotions.surprise<< ",";
			outputFile << it->second.emotions.contempt<< ",";

			outputFile << it->second.expressions.smile<< ",";
			outputFile << it->second.expressions.innerBrowRaise<< ",";
			outputFile << it->second.expressions.browRaise<< ",";
			outputFile << it->second.expressions.browFurrow<< ",";
			outputFile << it->second.expressions.noseWrinkle<< ",";
			outputFile << it->second.expressions.upperLipRaise<< ",";
			outputFile << it->second.expressions.lipCornerDepressor<< ",";
			outputFile << it->second.expressions.chinRaise<< ",";
			outputFile << it->second.expressions.lipPucker<< ",";
			outputFile << it->second.expressions.lipPress<< ",";
			outputFile << it->second.expressions.lipSuck<< ",";
			outputFile << it->second.expressions.mouthOpen<< ",";
			outputFile << it->second.expressions.smirk<< ",";
			outputFile << it->second.expressions.eyeClosure<< ",";
			outputFile << it->second.expressions.eyeWiden<< ",";
			outputFile << it->second.expressions.cheekRaise<< ",";
			outputFile << it->second.expressions.lidTighten<< ",";
			outputFile << it->second.expressions.dimpler<< ",";
			outputFile << it->second.expressions.lipStretch<< ",";
			outputFile << it->second.expressions.jawDrop<< "\n";
		}	
	}
    
    virtual void onImageCapture(Frame image){
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
	std::shared_ptr<ProcessStatusListener> ps2(new MyListener());
	detector.setProcessStatusListener(ps2.get());
	std::shared_ptr<ImageListener> ps3(new ImageList());
	detector.setImageListener(ps3.get());	
	std::shared_ptr<FaceListener> psl(new FaceList());
	detector.setFaceListener(psl.get());	

	//set detector for desired metrics
	detector.setDetectAllExpressions(true);
	detector.setDetectAllEmotions(true);
	outputFile.open(argsv[2]);
	faceFile.open(argsv[3]);
	faceFile<< "Timestamp, Found/Lost\n";
	//start the detector
	detector.start();

	//process the video file
	detector.process(argsv[1]);
	
	while(!done){
	}
	detector.stop();

	outputFile.close();
	faceFile.close();
	//delete ps2;
	//delete ps3;
	return 0;

}
