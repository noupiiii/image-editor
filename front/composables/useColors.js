export function useColors() {
  const hexToRGB = (hex) => {
    hex = hex.replace(/^#/, '');

    if (hex.length === 3) {
      hex = hex.split('').map(char => char + char).join('');
    }

    // Extraction des composantes hexadécimales
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);

    const rgbString = `rgb(${r},${g},${b})`;
    return rgbString;
  };

  return {
    hexToRGB
  };
}
