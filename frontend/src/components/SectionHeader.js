import React from "react";

const SectionHeader = ({ title, subtitle }) => (
  <div className="text-center px-5 pt-5">
    <h2>{title}</h2>
    <p className="px-5 py-2">{subtitle}</p>
  </div>
);

export default SectionHeader;
