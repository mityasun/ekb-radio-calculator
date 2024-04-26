import clsx from 'clsx';
import s from './dateIntervalPicker.module.css';
import { ROW_HEADERS } from './mockData';
import { getDaysInMonth } from 'shared/utils';
import { useState } from 'react';
import { useAdSettings } from 'shared/store';

const ROW_HEADERS_HEADER = 'интервал времени';
const ROW_HEADERS_FOOTER = 'итого';
const BOADCAST_QUANTITY = 'количество трансляций';
const TIMING_QUANTITY = 'общий хронометраж';
const rowHeaders = ROW_HEADERS;
const daysInMonth = getDaysInMonth(1, 2024);
const timeUnit = 'сек';

const rowBroadcastQuantity = 1;
const totalBroadcastQuantity = 15;

const rowTimingQuantity = 1;
const totalTimingQuantity = 15;

export const DateIntervalPicker = () => {
  const { adSettings } = useAdSettings();

  const audio_duration = adSettings.audio_duration?.audio_duration ?? 0;

  const [selectedCells, setSelectedCells] = useState<Record<string, number>>({});

  const handleCellClick = (day: number, row: number) => {
    const currentAudioDuration = audio_duration;
    setSelectedCells((prevState) => {
      const key = `${row}-${day}`;
      if (prevState[key]) {
        const { [key]: _, ...newState } = prevState;
        return newState;
      } else {
        return {
          ...prevState,
          [key]: currentAudioDuration
        };
      }
    });
  };

  return (
    <div className={clsx(s.dateIntervalPicker)}>
      <div className={clsx(s.rowHeaders)}>
        <div>{ROW_HEADERS_HEADER}</div>
        {rowHeaders.map((row) => (
          <div key={row.id}>{row.time_interval}</div>
        ))}
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
        {rowHeaders.map((row) => (
          <div className={clsx(s.tableRow)} key={row.id}>
            {daysInMonth.map((day) => (
              <div
                className={clsx(
                  day.isWeekend && s.weekend,
                  s.tableCell,
                  selectedCells[`${row.id}-${day.date}`] && s.selectedCell
                )}
                key={day.date}
                onClick={() => handleCellClick(day.date, row.id)}>
                {selectedCells[`${row.id}-${day.date}`] && selectedCells[`${row.id}-${day.date}`]}
              </div>
            ))}
            <div className={clsx(s.tableCellCounter)}>{rowBroadcastQuantity}</div>
            <div className={clsx(s.tableCellTotal)}>{rowTimingQuantity + ' ' + timeUnit}</div>
          </div>
        ))}
        <div className={clsx(s.tableRowTotal)}>
          {daysInMonth.map((day) => (
            <div className={clsx(day.isWeekend && s.weekend)} key={day.date}></div>
          ))}
          <div className={clsx(s.tableCellCounter)}>{totalBroadcastQuantity}</div>
          <div className={clsx(s.tableCellTotal)}>{totalTimingQuantity + ' ' + timeUnit}</div>
        </div>
      </div>
    </div>
  );
};
