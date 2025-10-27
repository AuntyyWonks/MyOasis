import React from 'react';

/**
 * A sign-in button with specific dimensions and styling.
 * Width: 92px
 * Height: 56px
 * Radius: 20px
 * Font Size: 20px
 */
const SignInButton = () => {
  return (
    <button
      className="
        w-24
        h-14
        absolute
        -right-96
        top-0
        bg-white
        rounded-2xl
        text-lg
        font-medium
        text-black
        flex
        items-center
        justify-center
        shadow-sm
        hover:bg-gray-100
        focus:outline-none
        focus:ring-2
        focus:ring-blue-500
        focus:ring-opacity-50
        transition-colors
      "
    >
      Sign In
    </button>
  );
};

export default SignInButton;