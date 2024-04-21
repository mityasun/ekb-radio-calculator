export const getDaysInMonth = (month: number, year: number) => {
  const date = new Date(year, month, 1);
  const days = [];
  const daysOfWeek = ['ВС', 'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ'];

  while (date.getMonth() === month) {
    const day = {
      date: date.getDate(),
      dayOfWeek: daysOfWeek[date.getDay()],
      isWeekend: [0, 6].includes(date.getDay())
    };
    days.push(day);
    date.setDate(date.getDate() + 1);
  }
  return days;
};
