import clsx from 'clsx';
import s from './mainPage.module.css';
import { LocationStationSelect } from 'widgets/locationStationSelect';
import { RadioStationDescription } from 'widgets/radioStationDescription';
import { RadioStationDataWidget } from 'widgets/radioStationDataWidget';
import { RadioAdCostCalculator } from 'widgets/radioAdCostCalculator';
import { useQuery } from '@tanstack/react-query';
import { Helmet } from 'react-helmet-async';
import { SystemText } from 'shared/types';

export const MainPage = () => {
  const { data: systemText } = useQuery<SystemText>({ queryKey: ['system-text'] });

  return (
    <div className={clsx(s.mainPage)}>
      <>
        <Helmet>
          <title>{systemText?.title && systemText.title}</title>
        </Helmet>
        <LocationStationSelect />
        <RadioStationDescription />
        <RadioStationDataWidget />
        <RadioAdCostCalculator />
      </>
    </div>
  );
};
