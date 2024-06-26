import clsx from 'clsx';
import s from './dateIntervalPicker.module.css';
import { getDaysInMonth } from 'shared/utils';
import { useStore } from 'shared/store';
import { useMemo } from 'react';
import { Tooltip } from 'react-tooltip';
import { DATA_INTERVAL_PICKER_CONTENT_TEXT, DATA_TOOLTIP_TEXT, toolTipStyle } from '../configs';

export const DateIntervalPicker = () => {
  const {
    appSettings,
    audioDurations,
    timeIntervals,
    selectedRadio,
    customer_selection,
    setCustomerSelection,
    deleteCustomerSelection
  } = useStore();

  const daysInMonth = getDaysInMonth(appSettings.month?.id);
  const isNotSelectedRadio = selectedRadio === null;
  const audioDurationId = appSettings.audio_duration?.id ?? 0;

  const findCustomerSelection = (date: number, time_interval: number) => {
    return customer_selection.find((cs) => cs.date === date && cs.time_interval === time_interval);
  };

  const getAudioDurationById = (idAudioDuration?: number) => {
    if (!audioDurations) return 0;
    return audioDurations.find((ad) => ad.id === idAudioDuration)?.audio_duration || 0;
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
    if (!selectedRadio) return;
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
        <div>{DATA_INTERVAL_PICKER_CONTENT_TEXT.ROW_HEADERS_HEADER}</div>
        {timeIntervals && timeIntervals.map((row) => <div key={row.id}>{row.time_interval}</div>)}
        <div>{DATA_INTERVAL_PICKER_CONTENT_TEXT.ROW_HEADERS_FOOTER}</div>
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
          <div className={clsx(s.scrollContainerCounter)}>{DATA_INTERVAL_PICKER_CONTENT_TEXT.BOADCAST_QUANTITY}</div>
          <div className={clsx(s.scrollContainerTotal)}>{DATA_INTERVAL_PICKER_CONTENT_TEXT.TIMING_QUANTITY}</div>
        </div>
        {timeIntervals &&
          timeIntervals.map((row) => (
            <div className={clsx(s.tableRow)} key={row.id}>
              {daysInMonth.map((day) => (
                <div
                  className={clsx(
                    day.isWeekend && s.weekend,
                    s.tableCell,
                    findCustomerSelection(day.date, row.id) && s.selectedCell
                  )}
                  key={day.date}
                  data-tooltip-id="table-cell"
                  data-tooltip-content={DATA_TOOLTIP_TEXT}
                  onClick={() => handleCellClick(day.date, row.id)}>
                  {findCustomerSelection(day.date, row.id) &&
                    getAudioDurationById(findCustomerSelection(day.date, row.id)?.audio_duration)}
                </div>
              ))}
              <div className={clsx(s.tableCellCounter)}>{rowBroadcastQuantity(row.id)}</div>
              <div className={clsx(s.tableCellTotal)}>
                {rowTimingQuantity(row.id) + ' ' + DATA_INTERVAL_PICKER_CONTENT_TEXT.UNIT_SECONDS}
              </div>
            </div>
          ))}
        <div className={clsx(s.tableRowTotal)}>
          {daysInMonth.map((day) => (
            <div className={clsx(day.isWeekend && s.weekend)} key={day.date}>
              {columnBroadcastQuantity(day.date)}
            </div>
          ))}
          <div className={clsx(s.tableCellCounter)}>{totalBroadcastQuantity()}</div>
          <div className={clsx(s.tableCellTotal)}>
            {totalTimingQuantity() + ' ' + DATA_INTERVAL_PICKER_CONTENT_TEXT.UNIT_SECONDS}
          </div>
        </div>
      </div>
      {isNotSelectedRadio && <Tooltip id="table-cell" place="top" style={toolTipStyle} />}
    </div>
  );
};
