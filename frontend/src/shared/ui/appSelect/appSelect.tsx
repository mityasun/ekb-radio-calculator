import { FC } from 'react';
import Select from 'react-select';
import './appSelect.css';

export interface AppSelectProps extends React.ComponentProps<typeof Select> {
  maxWidth: string;
}

export const AppSelect: FC<AppSelectProps> = ({ maxWidth, ...props }) => {
  return (
    <Select
      styles={{ container: (base) => ({ ...base, maxWidth }) }}
      className="app-select"
      classNamePrefix="app-select"
      {...props}
    />
  );
};
