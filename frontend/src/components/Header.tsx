import { useState } from 'react';
import axios from 'axios';
import ResetBtn from './ResetBtn';

type Props = {
  setMessages: any;
};

const Header = ({ setMessages }: Props) => {
  const [isResetting, setIsResetting] = useState(false);

  const resetConvo = async () => {
    setIsResetting(true);

    await axios
      .get('http://localhost:8000/reset')
      .then((res) => {
        if (res.status === 200) {
          setMessages([]);
        } else {
          console.error('Error with API call');
        }
      })
      .catch((error) => {
        console.error(error.message);
      });

    setIsResetting(false);
  };

  return (
    <div className='flex justify-between items-center w-full p-4 bg-slate-900 font-bold shadow'>
      <p className='text-purple-300'>Bella</p>
      <button
        className={
          'transition-all duration-300 text-violet-300 hover:text-pink-300 ' +
          (isResetting && 'animate-pulse')
        }
        onClick={resetConvo}
      >
        <ResetBtn />
      </button>
    </div>
  );
};

export default Header;
