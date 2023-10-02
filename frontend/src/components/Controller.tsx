import { useState } from 'react';
import axios from 'axios';
import Header from './Header';
import Recorder from './Recorder';

const Controller = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);

  const createBlobURL = (data: any) => {
    // handles backend stream of data and coverts it to audio
    const blob = new Blob([data], { type: 'audio/mpeg' });
    const url = window.URL.createObjectURL(blob);
    return url;
  };

  const handleStop = async (blobURL: string) => {
    setIsLoading(true);

    // add msg to messages
    const myMessage = { sender: 'me', blobURL };
    const messagesArray = [...messages, myMessage];

    // convert blobURL to blobObj
    fetch(blobURL)
      .then((res) => res.blob())
      .then(async (blob) => {
        // build audio to send to backend
        const formData = new FormData();
        formData.append('file', blob, 'my_file.wav');

        // send to endpoint
        await axios
          .post('http:localhost:8000/post-audio', formData, {
            headers: {
              'Content-Type': 'audio/mpeg',
            },
            responseType: 'arraybuffer',
          })
          .then((res: any) => {
            const blob = res.data;
            const audio = new Audio();
            audio.src = createBlobURL(blob);

            // add to audio
            const bellaMessage = { sender: 'bella', blobURL: audio.src };
            messagesArray.push(bellaMessage);
            setMessages(messagesArray);

            setIsLoading(false);
            audio.play();
          })
          .catch((error) => {
            console.error(error.message);
            setIsLoading(false);
          });
      });

    setIsLoading(false);
  };

  return (
    <div className='h-screen overflow-y-hidden'>
      <Header setMessages={setMessages} />
      <div className='flex flex-col justify-between h-full overflow-y-scroll pb-96'>
        <div className='mt-5 px-5'>
          {messages?.map((audio, index) => {
            return (
              <div
                key={index + audio.sender}
                className={
                  'flex flex-col ' +
                  (audio.sender === 'bella' && 'flex items-end')
                }
              >
                {/* Sender */}
                <div className='mt-4 '>
                  <p
                    className={
                      audio.sender === 'bella'
                        ? 'text-right mr-2 text-pink-800'
                        : 'ml-2 text-violet-800'
                    }
                  >
                    {audio.sender}
                  </p>

                  {/* Message */}
                  <audio
                    src={audio.blobURL}
                    className='appearance-none'
                    controls
                  />
                </div>
              </div>
            );
          })}

          {messages.length == 0 && !isLoading && (
            <div className='text-center text-violet-800  font-light mt-10'>
              Send Bella a message...
            </div>
          )}

          {isLoading && (
            <div className='text-center text-pink-800 font-light mt-10 animate-pulse'>
              Gimme a few seconds...
            </div>
          )}
        </div>
        <Recorder handleStop={handleStop} />
      </div>
    </div>
  );
};

export default Controller;
