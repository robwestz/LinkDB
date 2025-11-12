const EmptyState = ({ message = 'No data found', icon = '📭' }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="text-6xl mb-4">{icon}</div>
      <p className="text-gray-600 dark:text-gray-400 text-lg">{message}</p>
    </div>
  );
};

export default EmptyState;
