import clsx from 'clsx';
import s from './locationStationSelect.module.css';
import { LocationSelect } from 'entities/locationSelect';
import { RadioStationSelect } from 'entities/radioStationSelect';

export const LocationStationSelect = () => {
  return (
    <div className={clsx(s.locationStationSelect)}>
      <LocationSelect />
      <RadioStationSelect />
    </div>
  );
};
