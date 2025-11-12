// Color helpers for charts and visualizations

// Score-based colors
export const getScoreColor = (score) => {
  if (score >= 80) return '#10b981'; // green-500
  if (score >= 60) return '#3b82f6'; // blue-500
  if (score >= 40) return '#f59e0b'; // amber-500
  return '#ef4444'; // red-500
};

// Risk level colors
export const getRiskColor = (risk) => {
  const riskColors = {
    high: '#ef4444', // red-500
    medium: '#f59e0b', // amber-500
    low: '#10b981', // green-500
  };

  return riskColors[risk] || riskColors.low;
};

// Status colors
export const getStatusColor = (status) => {
  const statusColors = {
    success: '#10b981',
    info: '#3b82f6',
    warning: '#f59e0b',
    danger: '#ef4444',
  };

  return statusColors[status] || statusColors.info;
};

// Chart color palettes
export const chartColors = {
  primary: [
    '#3b82f6', // blue-500
    '#10b981', // green-500
    '#f59e0b', // amber-500
    '#ef4444', // red-500
    '#8b5cf6', // violet-500
    '#ec4899', // pink-500
    '#06b6d4', // cyan-500
    '#f97316', // orange-500
  ],
  gradient: [
    '#6366f1', // indigo-500
    '#8b5cf6', // violet-500
    '#a855f7', // purple-500
    '#d946ef', // fuchsia-500
    '#ec4899', // pink-500
  ],
};

// Generate color based on index
export const getColorByIndex = (index, palette = 'primary') => {
  const colors = chartColors[palette] || chartColors.primary;
  return colors[index % colors.length];
};

// Generate gradient stops for backgrounds
export const getGradient = (score) => {
  if (score >= 80) return 'from-green-500 to-emerald-600';
  if (score >= 60) return 'from-blue-500 to-indigo-600';
  if (score >= 40) return 'from-amber-500 to-orange-600';
  return 'from-red-500 to-rose-600';
};

// Alpha/opacity variations
export const withOpacity = (color, opacity) => {
  // Assumes hex color format #RRGGBB
  if (color.startsWith('#')) {
    const r = parseInt(color.slice(1, 3), 16);
    const g = parseInt(color.slice(3, 5), 16);
    const b = parseInt(color.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${opacity})`;
  }
  return color;
};
