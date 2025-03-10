"use client";

import dynamic from "next/dynamic";

// Export the mad dynamically to get rid of ssr error
const WrappedMap = dynamic(() => import("./Map"), { ssr: false });

const MapWrapper = () => {
  return <WrappedMap />;
};

export default MapWrapper;
