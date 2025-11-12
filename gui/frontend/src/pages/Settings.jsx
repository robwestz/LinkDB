import React from 'react';
import Card from '../components/common/Card';
import Button from '../components/common/Button';

const Settings = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Settings</h1>

      <Card title="Database Configuration" className="mb-6">
        <p className="text-gray-600 mb-4">Database path and backup settings</p>
        <Button>Configure</Button>
      </Card>

      <Card title="Analysis Thresholds">
        <p className="text-gray-600 mb-4">Customize warning thresholds</p>
        <Button>Edit Thresholds</Button>
      </Card>
    </div>
  );
};

export default Settings;
