const Skeleton = ({ className = '', width = '100%', height = '20px' }) => {
  return (
    <div
      className={`animate-pulse bg-gray-200 dark:bg-gray-700 rounded ${className}`}
      style={{ width, height }}
    />
  );
};

export default Skeleton;
