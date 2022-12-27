/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/naming-convention */
/* eslint-disable react/button-has-type */
/* eslint-disable react/react-in-jsx-scope */
import React, { useState } from 'react';
import { Pixel, User } from './interfaces/Pixels.interfaces';
import './App.css';

const m_dimension_x = 96;
const m_dimension_y = 64;

const top_placers: User[] = [] as User[];

const Table = ({ pixels }: { pixels: Pixel[][] }) => (
  <table style={{ border: '1px solid black', width: '100%' }}>
    <tbody>
      <tr>
        <th>X</th>
        {pixels[0].map((_, x) => (<th key={`head${x.toString().padStart(2, '0')}`}>{x + 1}</th>))}
      </tr>
      {
        pixels.map((pixelrow, y) => (
          <tr key={`row${y.toString().padStart(2, '0')}`}>
            <td key={`headR${y.toString().padStart(2, '0')}`}>{y + 1}</td>
            {
                pixelrow.map((pixel, x) => (
                  <td
                    key={
                      `row${y.toString().padStart(2, '0')}col${x.toString().padStart(2, '0')}`
                    }
                    style={
                      {
                        backgroundColor: pixel.color,
                        width: '5px',
                        height: '5px',
                      }
                    }
                  />
                ))
              }
          </tr>
        ))
      }
    </tbody>
  </table>
);

const isValidColor = (color: string) => (
  /^#([0-9A-F]{3}){1,2}$/i.test(color)
  || color in window.getComputedStyle(document.body)
);

const DebugCommandLine = (
  { setPixels }: { setPixels: React.Dispatch<React.SetStateAction<Pixel[][]>> },
) => {
  const [inputText, setInputText] = useState('');
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(event.target.value);
  };
  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      setPixels((pixels) => {
        const newpixels = [...pixels];

        if (!inputText.toLowerCase().startsWith('set')) return pixels;
        const params = inputText.substring(4).split(' ');
        const x: number = Number.parseInt(params[1], 10) - 1;
        const y: number = Number.parseInt(params[0], 10) - 1;
        const color = params[2];
        if (!isValidColor(color)) return pixels;
        const placer = { username: 'commandline', id: 'cl0', placed: 1 } as User;
        newpixels[y][x].color = color;
        newpixels[y][x].placer = placer;
        newpixels[y][x].timestamp = Date.now();
        const l_placer = top_placers.find((p) => p.id === placer.id);
        if (!l_placer) top_placers.push(placer);
        else top_placers[top_placers.indexOf(l_placer)].placed += 1;
        return newpixels;
      });
      setInputText('');
    }
  };
  return (
    <input onKeyDown={handleKeyDown} onChange={handleChange} value={inputText} type="text" />
  );
};

const App = () => {
  // pixels[row][column]
  const m_pixels: Pixel[][] = Array.from(
    Array(m_dimension_y),
    () => Array(m_dimension_x)
      .fill({ color: '#ffffff', placer: '_initial', time: Date.now() }),
  );
  const [pixels, setPixels] = useState(m_pixels);
  return (
    <div className="App">
      <Table pixels={pixels} />
      <DebugCommandLine setPixels={setPixels} />
    </div>
  );
};

export default App;
