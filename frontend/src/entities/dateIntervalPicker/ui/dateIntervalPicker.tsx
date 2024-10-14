import clsx from 'clsx';
import s from './dateIntervalPicker.module.css';
import { getDaysInMonth } from 'shared/utils';
import { useStore } from 'shared/store';
import { useEffect, useMemo, useState } from 'react';
import { Tooltip } from 'react-tooltip';
import { DATA_INTERVAL_PICKER_CONTENT_TEXT, DATA_TOOLTIP_TEXT, toolTipStyle } from '../configs';
import { InvalidSetModal } from 'widgets/invalidSetModal';

export const DateIntervalPicker = () => {
  const appSettings = useStore((state) => state.appSettings);
  const timeIntervals = useStore((state) => state.timeIntervals);
  const selectedRadio = useStore((state) => state.selectedRadio);
  const customer_selection = useStore((state) => state.customer_selection);
  const setCustomerSelection = useStore((state) => state.setCustomerSelection);
  const deleteCustomerSelection = useStore((state) => state.deleteCustomerSelection);
  const blockPositions = useStore((state) => state.blockPositions);
  const audioDurations = useStore((state) => state.audioDurations);
  const [isInvalidSetModalOpen, setInvalidSetModalOpen] = useState<boolean>(false);
  const daysInMonth = getDaysInMonth(appSettings.month?.id);
  const isNotSelectedRadio = selectedRadio === null;
  const audioDurationId = appSettings.audio_duration?.id ?? 0;
  const selectedRadioAudioDurationsIds = audioDurations?.map((ad) => ad.id) ?? [];
  const selectedRadioBlockPositionsIds = appSettings.block_position?.id;
  const selectedRadioTimeIntervalsIds = timeIntervals?.map((ti) => ti.id) ?? [];
  const selectedRadioMonthIds = selectedRadio?.month_rate.map((mr) => mr.id) ?? [];
  const isSelectedAudioDuratiosValid = customer_selection
    .map((cs) => selectedRadioAudioDurationsIds.includes(cs.audio_duration))
    .includes(false)
    ? false
    : true;

  const isSelectedTimeIntervalsValid = customer_selection
    .map((cs) => selectedRadioTimeIntervalsIds.includes(cs.time_interval))
    .includes(false)
    ? false
    : true;

  const isSelectedMonthValid = appSettings.month && selectedRadioMonthIds.includes(appSettings.month.id);

  const isSelectedBlockPositionsValid =
    selectedRadioBlockPositionsIds && blockPositions?.map((bp) => bp.id).includes(selectedRadioBlockPositionsIds);

  const isValidSet =
    (Boolean(!appSettings.audio_duration) ||
      (isSelectedAudioDuratiosValid &&
        isSelectedTimeIntervalsValid &&
        isSelectedMonthValid &&
        isSelectedBlockPositionsValid)) ??
    true;

  const findCustomerSelection = (date: number, time_interval: number) => {
    return customer_selection.find((cs) => cs.date === date && cs.time_interval === time_interval);
  };

  const getAudioDurationById = (idAudioDuration?: number) => {
    if (!audioDurations) return 0;
    return audioDurations.find((ad) => ad.id === idAudioDuration)?.audio_duration || 0;
  };

  useEffect(() => {
    setInvalidSetModalOpen(Boolean(!isValidSet));
  }, [isValidSet]);

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
    if (!selectedRadio || !isValidSet) return;
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

  const handleCloseInvalidSetModal = () => {
    setInvalidSetModalOpen(false);
  };

  return (
    <>
      <div className={clsx(s.dateIntervalPicker, !isValidSet && s.invalidSet)}>
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
                      Boolean(getAudioDurationById(findCustomerSelection(day.date, row.id)?.audio_duration)) &&
                        s.selectedCell
                    )}
                    key={day.date}
                    data-tooltip-id="table-cell"
                    data-tooltip-content={DATA_TOOLTIP_TEXT}
                    onClick={() => handleCellClick(day.date, row.id)}>
                    {findCustomerSelection(day.date, row.id) &&
                      Boolean(getAudioDurationById(findCustomerSelection(day.date, row.id)?.audio_duration)) &&
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
      <InvalidSetModal isOpen={isInvalidSetModalOpen} onClose={handleCloseInvalidSetModal} />
    </>
  );
};
