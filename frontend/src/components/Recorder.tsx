import { ReactMediaRecorder } from 'react-media-recorder';
import RecorderIcon from './RecorderIcon';

type Props = {
  handleStop: any;
};

const Recorder = ({ handleStop }: Props) => {
  return (
    <>
      <div className='fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-violet-800 to-pink-800'>
        <div className='flex justify-center items-center w-full'>
          <ReactMediaRecorder
            audio
            onStop={handleStop}
            render={({ status, startRecording, stopRecording }) => (
              <div className='mt-2'>
                <button
                  className='bg-white p-4 rounded-full'
                  onMouseDown={startRecording}
                  onMouseUp={stopRecording}
                >
                  <RecorderIcon
                    classText={
                      status === 'recording'
                        ? 'animate-pulse text-red-500'
                        : 'text-violet-800'
                    }
                  />
                </button>
                <p className='mt-2 text-pink-100 font-light'>{status}</p>
              </div>
            )}
          />
        </div>
      </div>
    </>
  );
};

export default Recorder;
