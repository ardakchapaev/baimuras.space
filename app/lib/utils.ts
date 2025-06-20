
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatCurrency(amount: number): string {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'KGS',
    minimumFractionDigits: 0,
  }).format(amount);
}

export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(d);
}

export function formatDateTime(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date;
  return new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(d);
}

export function getStatusColor(status: string): string {
  const statusColors: Record<string, string> = {
    // Lead statuses
    new: 'bg-blue-100 text-blue-800',
    contacted: 'bg-yellow-100 text-yellow-800',
    qualified: 'bg-purple-100 text-purple-800',
    converted: 'bg-green-100 text-green-800',
    lost: 'bg-red-100 text-red-800',
    
    // Project statuses
    planning: 'bg-blue-100 text-blue-800',
    in_progress: 'bg-amber-100 text-amber-800',
    completed: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
    
    // Order statuses
    pending: 'bg-gray-100 text-gray-800',
    confirmed: 'bg-blue-100 text-blue-800',
    in_production: 'bg-yellow-100 text-yellow-800',
    ready: 'bg-purple-100 text-purple-800',
    delivered: 'bg-green-100 text-green-800',
    
    // Payment statuses
    failed: 'bg-red-100 text-red-800',
    refunded: 'bg-orange-100 text-orange-800',
    
    // Measurement statuses
    scheduled: 'bg-blue-100 text-blue-800',
    rescheduled: 'bg-yellow-100 text-yellow-800',
    
    // Estimate statuses
    draft: 'bg-gray-100 text-gray-800',
    sent: 'bg-blue-100 text-blue-800',
    approved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    expired: 'bg-orange-100 text-orange-800',
  };
  
  return statusColors[status] || 'bg-gray-100 text-gray-800';
}

export function getStatusBadge(status: string): string {
  const statusNames: Record<string, string> = {
    new: 'Новый',
    contacted: 'Связались',
    qualified: 'Квалифицирован',
    converted: 'Конвертирован',
    lost: 'Потерян',
    planning: 'Планирование',
    in_progress: 'В работе',
    completed: 'Завершен',
    cancelled: 'Отменен',
    pending: 'Ожидает',
    confirmed: 'Подтвержден',
    in_production: 'В производстве',
    ready: 'Готов',
    delivered: 'Доставлен',
    failed: 'Неудачно',
    refunded: 'Возврат',
    scheduled: 'Запланирован',
    rescheduled: 'Перенесен',
    draft: 'Черновик',
    sent: 'Отправлен',
    approved: 'Одобрен',
    rejected: 'Отклонен',
    expired: 'Истек',
  };
  
  return statusNames[status] || status;
}

export function generateOrderNumber(): string {
  const prefix = 'BM';
  const timestamp = Date.now().toString().slice(-6);
  const random = Math.floor(Math.random() * 100).toString().padStart(2, '0');
  return `${prefix}${timestamp}${random}`;
}

export function calculatePercentageChange(current: number, previous: number): number {
  if (previous === 0) return current > 0 ? 100 : 0;
  return ((current - previous) / previous) * 100;
}

export function truncateText(text: string, length: number): string {
  if (text.length <= length) return text;
  return text.substring(0, length) + '...';
}
