import React from 'react';

const About = () => {
  const missionHeadline = "Our Mission";
  const missionSubheadline = "To make gardening accessible, enjoyable, and successful for everyone, regardless of their experience level.";

  const missionPoints = [
    {
      imageSrc: "/expert-knowledge.jpg",
      headline: "Expert Knowledge",
      subheadline: "AI-powered insights backed by horticultural expertise",
    },
    {
      imageSrc: "/personalized-care.jpeg",
      headline: "Personalized Care",
      subheadline: "Tailored advice for your specific plants and environment",
    },
    {
      imageSrc: "/sustainable-growth.jpeg",
      headline: "Sustainable Growth",
      subheadline: "Promoting eco-friendly gardening practices",
    },
  ];

  return (
    <section className="h-screen py-16 px-4 bg-white text-black">
      <div className="text-center mb-16">
        <h2 className="text-[48px] font-bold mb-4">
          {missionHeadline}
        </h2>
        <p className="text-base text-black/50 text-center">
          {missionSubheadline}
        </p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-7xl mx-auto">
        {missionPoints.map((point, index) => (
          <div key={index} className="flex flex-col items-center text-center">
            <img 
              src={point.imageSrc} 
              alt={point.headline} 
              className="w-full h-full object-cover mb-6 rounded-lg"
            />
            <h3 className="text-lg font-semibold mb-2">
              {point.headline}
            </h3>
            {/* Subheadline */}
            <p className="text-xs font-light text-black/60 px-4">
              {point.subheadline}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default About;