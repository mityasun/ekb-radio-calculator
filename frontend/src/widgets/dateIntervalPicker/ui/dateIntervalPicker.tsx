import clsx from 'clsx';
import s from './dateIntervalPicker.module.css';
import { getDaysInMonth } from 'shared/utils';
import { useAdSettingsStore } from 'shared/store';
import { useOrder } from 'shared/store/orderStore';
import { useQuery } from '@tanstack/react-query';
import { getTimeIntervals } from '../api';

const ROW_HEADERS_HEADER = 'интервал времени';
const ROW_HEADERS_FOOTER = 'итого';
const BOADCAST_QUANTITY = 'количество трансляций';
const TIMING_QUANTITY = 'общий хронометраж';
const timeUnit = 'сек';

export const DateIntervalPicker = () => {
  const { adSettings } = useAdSettingsStore();
  const { customer_selection, setCustomerSelection, deleteCustomerSelection } = useOrder();
  const { data: rowHeaders } = useQuery({
    queryKey: ['time-intervals'],
    queryFn: getTimeIntervals
  });
  const daysInMonth = getDaysInMonth(adSettings.month?.id);

  const audio_duration = adSettings.audio_duration?.audio_duration ?? 0;

  const rowBroadcastQuantity = (timeInterval: number) => {
    const timeIntervalSelected = customer_selection.filter((cs) => cs.time_interval === timeInterval);
    return timeIntervalSelected ? timeIntervalSelected.length : 0;
  };

  const columnBroadcastQuantity = (date: number) => {
    const dateSelected = customer_selection.filter((cs) => cs.date === date);
    return dateSelected ? dateSelected.length : 0;
  };

  const rowTimingQuantity = (timeInterval: number) => {
    const timeIntervalSelected = customer_selection.filter((cs) => cs.time_interval === timeInterval);
    return timeIntervalSelected ? timeIntervalSelected.reduce((a, b) => a + b.audio_duration, 0) : 0;
  };

  const totalBroadcastQuantity = () => {
    return customer_selection ? customer_selection.length : 0;
  };

  const totalTimingQuantity = () => {
    return customer_selection ? customer_selection.reduce((a, b) => a + b.audio_duration, 0) : 0;
  };

  const handleCellClick = (date: number, time_interval: number) => {
    const currentAudioDuration = audio_duration;
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
                  {customer_selection.find((cs) => cs.date === day.date && cs.time_interval === row.id) &&
                    customer_selection.find((cs) => cs.date === day.date && cs.time_interval === row.id)
                      ?.audio_duration}
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
