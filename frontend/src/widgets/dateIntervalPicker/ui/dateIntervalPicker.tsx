import clsx from 'clsx';
import s from './dateIntervalPicker.module.css';
import { getDaysInMonth } from 'shared/utils';
import { useAdSettingsStore, useOrderStore } from 'shared/store';
import { useQuery } from '@tanstack/react-query';
import { getTimeIntervals } from '../api';
import { AdDuration } from 'shared/types';
import { useMemo } from 'react';

const ROW_HEADERS_HEADER = 'интервал времени';
const ROW_HEADERS_FOOTER = 'итого';
const BOADCAST_QUANTITY = 'количество трансляций';
const TIMING_QUANTITY = 'общий хронометраж';
const timeUnit = 'сек';

export const DateIntervalPicker = () => {
  const { adSettings } = useAdSettingsStore();
  const { customer_selection, setCustomerSelection, deleteCustomerSelection } = useOrderStore();
  const { data: rowHeaders } = useQuery({ queryKey: ['time-intervals'], queryFn: getTimeIntervals });
  const { data: audioDuration } = useQuery<AdDuration[]>({ queryKey: ['audio-durations'] });

  const daysInMonth = getDaysInMonth(adSettings.month?.id);

  const audioDurationId = adSettings.audio_duration?.id ?? 0;

  const findCustomerSelection = (date: number, time_interval: number) => {
    return customer_selection.find((cs) => cs.date === date && cs.time_interval === time_interval);
  };

  const getAudioDurationById = (idAudioDuration?: number) => {
    if (!audioDuration) return 0;
    return audioDuration.find((ad) => ad.id === idAudioDuration)?.audio_duration || 0;
  };

  const rowBroadcastQuantity = useMemo(
    () => (timeInterval: number) => {
      const timeIntervalSelected = customer_selection.filter((cs) => cs.time_interval === timeInterval);
      return timeIntervalSelected ? timeIntervalSelected.length : 0;
    },
    [customer_selection]
  );

  const columnBroadcastQuantity = useMemo(
    () => (date: number) => {
      const dateSelected = customer_selection.filter((cs) => cs.date === date);
      return dateSelected ? dateSelected.length : 0;
    },
    [customer_selection]
  );

  const rowTimingQuantity = useMemo(
    () => (timeInterval: number) => {
      const timeIntervalSelected = customer_selection.filter((cs) => cs.time_interval === timeInterval);
      return timeIntervalSelected
        ? timeIntervalSelected.reduce((a, b) => a + getAudioDurationById(b.audio_duration), 0)
        : 0;
    },
    [customer_selection]
  );

  const totalBroadcastQuantity = useMemo(
    () => () => {
      return customer_selection ? customer_selection.length : 0;
    },
    [customer_selection]
  );

  const totalTimingQuantity = useMemo(
    () => () => {
      return customer_selection
        ? customer_selection.reduce((a, b) => a + getAudioDurationById(b.audio_duration), 0)
        : 0;
    },
    [customer_selection]
  );

  const handleCellClick = (date: number, time_interval: number) => {
    const currentAudioDuration = audioDurationId;
    if (customer_selection.find((cs) => cs.date === date && cs.time_interval === time_interval)) {
      deleteCustomerSelection({
        date,
        time_interval,
        audio_duration: currentAudioDuration
      });
    } else {
      setCustomerSelection({
        date,
        time_interval,
        audio_duration: currentAudioDuration
      });
    }
  };

  return (
    <div className={clsx(s.dateIntervalPicker)}>
      <div className={clsx(s.rowHeaders)}>
        <div>{ROW_HEADERS_HEADER}</div>
        {rowHeaders && rowHeaders.map((row) => <div key={row.id}>{row.time_interval}</div>)}
        <div>{ROW_HEADERS_FOOTER}</div>
      </div>
      <div className={clsx(s.scrollContainer)}>
        <div className={clsx(s.columHeaders)}>
          {daysInMonth.map((day) => (
            <div className={clsx(day.isWeekend && s.weekend)} key={day.date}>
              {day.date}
              <br />
              {day.dayOfWeek}
            </div>
          ))}
          <div className={clsx(s.scrollContainerCounter)}>{BOADCAST_QUANTITY}</div>
          <div className={clsx(s.scrollContainerTotal)}>{TIMING_QUANTITY}</div>
        </div>
        {rowHeaders &&
          rowHeaders.map((row) => (
            <div className={clsx(s.tableRow)} key={row.id}>
              {daysInMonth.map((day) => (
                <div
                  className={clsx(
                    day.isWeekend && s.weekend,
                    s.tableCell,
                    customer_selection.find((cs) => cs.date === day.date && cs.time_interval === row.id) &&
                      s.selectedCell
                  )}
                  key={day.date}
                  onClick={() => handleCellClick(day.date, row.id)}>
                  {findCustomerSelection(day.date, row.id) &&
                    getAudioDurationById(findCustomerSelection(day.date, row.id)?.audio_duration)}
                </div>
              ))}
              <div className={clsx(s.tableCellCounter)}>{rowBroadcastQuantity(row.id)}</div>
              <div className={clsx(s.tableCellTotal)}>{rowTimingQuantity(row.id) + ' ' + timeUnit}</div>
            </div>
          ))}
        <div className={clsx(s.tableRowTotal)}>
          {daysInMonth.map((day) => (
            <div className={clsx(day.isWeekend && s.weekend)} key={day.date}>
              {columnBroadcastQuantity(day.date)}
            </div>
          ))}
          <div className={clsx(s.tableCellCounter)}>{totalBroadcastQuantity()}</div>
          <div className={clsx(s.tableCellTotal)}>{totalTimingQuantity() + ' ' + timeUnit}</div>
        </div>
      </div>
    </div>
  );
};
