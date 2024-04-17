import { FC } from 'react';
import Select from 'react-select';
import './appSelect.css';

export type AppSelectOption = {
  value: string;
  label: string;
};

export const AppSelect: FC<React.ComponentProps<typeof Select>> = ({ ...props }) => {
  return <Select className="app-select" classNamePrefix="app-select" {...props} />;
};
