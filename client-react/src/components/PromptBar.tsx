import React from 'react'

function PromptBar() {
  return (
    <div className="w-full h-34 flex flex-col justify-between rounded-[2.5rem] border border-white/35 backdrop-blur-[1.5px] bg-black/15">
      <div className='w-40 h-10'></div>
      <div className='h-10 flex items-start justify-between gap-2 px-5 bg-yellow-500/0 text-[#B4B4AE] text-sm'>
        <div className='flex items-start gap-2'>
          <button className='p-2 rounded-full bg-[#232323] border border-[#70706F] cursor-pointer'><img src='/icons/add.svg' alt='add-icon' width={10} height={10} /></button>
          <button className='rounded-full bg-[#232323] flex items-center px-3 py-1 gap-1 border border-[#70706F] cursor-pointer'>
            <img src="/icons/gallery.svg" alt="gallery-icon" />
            <span>Attach</span>
          </button>
          <button className='rounded-full bg-[#232323] flex items-center px-3 py-1 gap-1 border border-[#70706F] cursor-pointer'>
            <img src="/icons/global.svg" alt="global-icon" />
            <span>Public</span>
          </button>
        </div>
        <div>
          <button className='p-2 rounded-full bg-[#70706F] border border-[#70706fc2] cursor-pointer'><img src='/icons/submit.svg' alt='submit-icon' width={8} height={8}/></button>
        </div>
      </div>
    </div>
  )
}

export default PromptBar