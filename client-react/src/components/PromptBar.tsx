import React, { useState } from 'react';

function PromptBar({ token }) {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await fetch('http://localhost:5000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token,
      },
      body: JSON.stringify({ message: prompt }),
    });

    if (res.ok) {
      const data = await res.json();
      setResponse(data.reply);
    } else {
      setResponse('Error communicating with the server.');
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit} className="w-full flex flex-col gap-4 py-4 justify-between rounded-[2.5rem] border border-white/35 backdrop-blur-[1.5px] bg-black/15">
        <textarea
          className='flex-1 ml-6 mr-12 bg-transparent outline-none resize-none text-gray-300 overflow-hidden'
          placeholder='Ask Oasis to help you plant...'
          rows={5}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        ></textarea>
        <div className='h-10 flex items-start justify-between gap-2 px-5 bg-yellow-500/0 text-[#B4B4AE] text-sm'>
          <div className='flex items-start gap-2'>
            <button type="button" className='p-2 rounded-full bg-[#232323] border border-[#70706F] cursor-pointer'><img src='/icons/add.svg' alt='add-icon' width={10} height={10} /></button>
            <button type="button" className='rounded-full bg-[#232323] flex items-center px-3 py-1 gap-1 border border-[#70706F] cursor-pointer'>
              <img src="/icons/gallery.svg" alt="gallery-icon" />
              <span>Attach</span>
            </button>
            <button type="button" className='rounded-full bg-[#232323] flex items-center px-3 py-1 gap-1 border border-[#70706F] cursor-pointer'>
              <img src="/icons/global.svg" alt="global-icon" />
              <span>Public</span>
            </button>
          </div>
          <div>
            <button type="submit" className='p-2 rounded-full bg-[#70706F] border border-[#70706fc2] cursor-pointer'><img src='/icons/submit.svg' alt='submit-icon' width={8} height={8}/></button>
          </div>
        </div>
      </form>
      {response && (
        <div className="mt-4 p-4 bg-gray-800 text-white rounded-lg">
          <h3 className="font-bold">Oasis says:</h3>
          <p>{response}</p>
        </div>
      )}
    </>
  );
}

export default PromptBar;