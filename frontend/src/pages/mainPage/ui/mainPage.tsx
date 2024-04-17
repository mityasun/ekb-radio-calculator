import clsx from 'clsx';
import s from './mainPage.module.css';
import { LocationStationSelect } from 'widgets/locationStationSelect';
import { RadioStationDescription } from 'widgets/radioStationDescription';
import { RadioStationDataWidget } from 'widgets/radioStationDataWidget';

export const MainPage = () => {
  return (
    <div className={clsx(s.mainPage)}>
      <LocationStationSelect />
      <RadioStationDescription />
      <RadioStationDataWidget />
    </div>
  );
};
