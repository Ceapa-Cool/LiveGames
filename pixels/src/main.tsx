import React from 'react';
import ReactDOM from 'react-dom/client';
import PixelCanvas from './PixelCanvas';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <PixelCanvas
    position={{ x: 50, y: 50 }} // absolute (x, y) position for canvas
    canvas_dimensions={{ width: 1600, height: 900 }} // canvas dimensions in px
    size={13} // general size multiplier
    grid_width={1} // grid line width
    grid_dimensions={{ width: 96, height: 64 }} // dimensions of the pixel grid itself
  />,
);
