import clsx from 'clsx';
import s from './radioAdCostCalculator.module.css';
import { AppSettingsSelector } from 'widgets/appSettingsSelector';
import { DateIntervalPicker } from 'entities/dateIntervalPicker';
import { ResultsAndSubmission } from 'entities/resultsAndSubmission';
import { useQuery } from '@tanstack/react-query';
import { SystemText } from 'shared/types';
import { DATE_INTERVAL_PICKER_TITLE } from '../configs';

export const RadioAdCostCalculator = () => {
  const { data: systemText } = useQuery<SystemText>({ queryKey: ['system-text'] });
  const markup = { __html: systemText?.disclaimer ? systemText.disclaimer : '' };

  return (
    <div className={clsx(s.radioAdCostCalculator)}>
      <h3 className={clsx(s.radioAdCostCalculatorTitle)}>{systemText?.title && systemText.title}</h3>
      <article className={clsx(s.radioAdCostCalculatorWelcome)} dangerouslySetInnerHTML={markup} />
      <AppSettingsSelector />
      <p>
        <b>{DATE_INTERVAL_PICKER_TITLE}</b>
      </p>
      <DateIntervalPicker />
      <ResultsAndSubmission />
    </div>
  );
};
