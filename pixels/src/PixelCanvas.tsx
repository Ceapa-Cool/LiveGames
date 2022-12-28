import React, { useEffect, useRef } from 'react';

interface Point {
  x: number;
  y: number;
}

interface Dimensions {
  width: number;
  height: number;
}

interface PixelCanvasProps {
  position: Point;
  canvas_dimensions: Dimensions;
  size: number;
  grid_dimensions: Dimensions;
  grid_width: number;
  grid_color?: string;
  bg_color?: string;
  tick_color?: string;
  padding?: number;
}

const PixelCanvas: React.FC<PixelCanvasProps> = ({
  position,
  size,
  canvas_dimensions,
  grid_dimensions,
  grid_width,
  grid_color = '#000000',
  bg_color = '#ffffff',
  tick_color = '#000000',
  padding = 20,
}) => {
  const pixels = Array.from(
    Array(grid_dimensions.height),
    () => Array(grid_dimensions.width).fill({
      color: '#ffffff',
      placer: '_init',
      timestamp: Date.now(),
    }),
  );

  const canvas_ref = useRef<HTMLCanvasElement>(null);
  const pixel_ratio = window.devicePixelRatio;

  // grid init
  useEffect(() => {
    const ctx = canvas_ref.current?.getContext('2d');
    if (!ctx) {
      return;
    }

    // this and the pixel ratio stuff is to avoid bad quality text rendering
    // https://stackoverflow.com/a/65124939/19161102
    ctx.scale(pixel_ratio, pixel_ratio);

    ctx.fillStyle = bg_color;
    ctx.fillRect(
      0,
      0,
      canvas_dimensions.width * pixel_ratio,
      canvas_dimensions.height * pixel_ratio,
    );

    ctx.strokeStyle = grid_color;
    ctx.lineWidth = grid_width;

    pixels.forEach((row, y_index) => {
      ctx.fillStyle = tick_color;
      ctx.textAlign = 'right';
      ctx.textBaseline = 'middle';

      ctx.fillText(
        (y_index + 1).toString(),
        padding - 5,
        padding + (y_index + 0.5) * size,
      );

      ctx.textAlign = 'center';
      ctx.textBaseline = 'bottom';

      row.forEach((pixel, x_index) => {
        ctx.fillStyle = tick_color;

        ctx.fillText(
          (x_index + 1).toString(),
          padding + (x_index + 0.5) * size,
          padding - 3,
        );

        ctx.fillStyle = pixel.color;

        ctx.fillRect(
          padding + x_index * size,
          padding + y_index * size,
          size,
          size,
        );
        ctx.strokeRect(
          padding + x_index * size,
          padding + y_index * size,
          size,
          size,
        );
      });
    });
  });

  return (
    <canvas
      ref={canvas_ref}
      width={canvas_dimensions.width * pixel_ratio}
      height={canvas_dimensions.height * pixel_ratio}
      style={{
        width: canvas_dimensions.width,
        height: canvas_dimensions.height,
        position: 'absolute',
        left: `${position.x}px`,
        top: `${position.y}px`,
        // these 3 are for visualizing boundaries for development
        borderStyle: 'solid',
        borderColor: 'black',
        borderWidth: '1px',
      }}
    />
  );
};

PixelCanvas.defaultProps = {
  grid_color: '#000000',
  bg_color: '#ffffff',
  tick_color: '#000000',
  padding: 20,
};

export default PixelCanvas;
