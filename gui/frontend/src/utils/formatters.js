// Date formatting
export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';

  try {
    const date = new Date(dateString);
    return date.toLocaleDateString('sv-SE', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return dateString;
  }
};

export const formatDateTime = (dateString) => {
  if (!dateString) return 'N/A';

  try {
    const date = new Date(dateString);
    return date.toLocaleString('sv-SE', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return dateString;
  }
};

// Number formatting
export const formatNumber = (num, decimals = 0) => {
  if (num === null || num === undefined) return 'N/A';

  return num.toLocaleString('sv-SE', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
};

export const formatPercent = (num, decimals = 1) => {
  if (num === null || num === undefined) return 'N/A';

  return `${num.toFixed(decimals)}%`;
};

export const formatScore = (score) => {
  if (score === null || score === undefined) return 'N/A';

  return `${score.toFixed(1)}/100`;
};

// Text formatting
export const truncate = (text, maxLength = 50) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;

  return `${text.substring(0, maxLength)}...`;
};

export const capitalize = (text) => {
  if (!text) return '';

  return text.charAt(0).toUpperCase() + text.slice(1);
};

// URL formatting
export const formatUrl = (url) => {
  if (!url) return '';

  try {
    const urlObj = new URL(url);
    return urlObj.hostname + urlObj.pathname;
  } catch {
    return url;
  }
};

// Score to status
export const getStatusFromScore = (score) => {
  if (score >= 80) return { label: 'Excellent', variant: 'success' };
  if (score >= 60) return { label: 'Good', variant: 'info' };
  if (score >= 40) return { label: 'Fair', variant: 'warning' };
  return { label: 'Poor', variant: 'danger' };
};

// Risk level formatting
export const formatRiskLevel = (risk) => {
  const riskMap = {
    high: { label: 'HIGH RISK', variant: 'danger', icon: '🚨' },
    medium: { label: 'Medium Risk', variant: 'warning', icon: '⚠️' },
    low: { label: 'Low Risk', variant: 'success', icon: '✅' },
  };

  return riskMap[risk] || riskMap.low;
};
