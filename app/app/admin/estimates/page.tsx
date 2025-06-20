
'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  Plus, 
  Search, 
  Calculator,
  FileText,
  Download,
  Eye,
  Edit,
  Copy,
  Send,
  Clock
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { formatCurrency, formatDate, getStatusColor, getStatusBadge } from '@/lib/utils';
import { Estimate } from '@/lib/types';

// Mock data
const mockEstimates: Estimate[] = [
  {
    id: '1',
    title: 'Кухонный гарнитур для квартиры',
    description: 'Современная кухня с островом, техника встроенная',
    totalAmount: 450000,
    validUntil: new Date('2024-02-28'),
    status: 'sent',
    notes: 'Включена установка и доставка',
    userId: 'user1',
    createdAt: new Date('2024-01-15'),
    updatedAt: new Date('2024-01-20'),
    user: {
      id: 'user1',
      username: 'manager1',
      email: 'manager@baimuras.space',
      name: 'Менеджер',
      createdAt: new Date(),
      updatedAt: new Date(),
      roles: []
    },
    estimateItems: [
      {
        id: '1',
        estimateId: '1',
        description: 'Кухонные шкафы верхние',
        quantity: 8,
        unitPrice: 25000,
        totalPrice: 200000
      },
      {
        id: '2',
        estimateId: '1',
        description: 'Кухонные шкафы нижние',
        quantity: 6,
        unitPrice: 30000,
        totalPrice: 180000
      },
      {
        id: '3',
        estimateId: '1',
        description: 'Столешница из кварца',
        quantity: 1,
        unitPrice: 70000,
        totalPrice: 70000
      }
    ]
  },
  {
    id: '2',
    title: 'Детская комната Монтессори',
    description: 'Безопасная мебель для развития ребенка',
    totalAmount: 180000,
    validUntil: new Date('2024-03-15'),
    status: 'draft',
    notes: 'Экологически чистые материалы',
    userId: 'user1',
    createdAt: new Date('2024-01-20'),
    updatedAt: new Date('2024-01-25'),
    user: {
      id: 'user1',
      username: 'manager1',
      email: 'manager@baimuras.space',
      name: 'Менеджер',
      createdAt: new Date(),
      updatedAt: new Date(),
      roles: []
    },
    estimateItems: []
  },
  {
    id: '3',
    title: 'Офисная мебель',
    description: 'Рабочие места для IT-команды',
    totalAmount: 320000,
    validUntil: new Date('2024-02-10'),
    status: 'approved',
    notes: 'Эргономичные решения',
    userId: 'user1',
    createdAt: new Date('2024-01-10'),
    updatedAt: new Date('2024-01-30'),
    user: {
      id: 'user1',
      username: 'manager1',
      email: 'manager@baimuras.space',
      name: 'Менеджер',
      createdAt: new Date(),
      updatedAt: new Date(),
      roles: []
    },
    estimateItems: []
  },
];

export default function EstimatesPage() {
  const [estimates, setEstimates] = useState<Estimate[]>(mockEstimates);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');

  const filteredEstimates = estimates.filter(estimate => {
    const matchesSearch = estimate.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         estimate.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || estimate.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'draft': return FileText;
      case 'sent': return Send;
      case 'approved': return Download;
      case 'rejected': return Clock;
      case 'expired': return Clock;
      default: return FileText;
    }
  };

  const isExpiringSoon = (validUntil: Date) => {
    const now = new Date();
    const daysDiff = Math.ceil((validUntil.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    return daysDiff <= 7 && daysDiff > 0;
  };

  const isExpired = (validUntil: Date) => {
    return new Date() > validUntil;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Сметы и расчеты</h1>
          <p className="text-slate-600">Создание и управление сметами для проектов</p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline" size="sm">
            <Calculator className="h-4 w-4 mr-2" />
            Калькулятор
          </Button>
          <Button size="sm">
            <Plus className="h-4 w-4 mr-2" />
            Новая смета
          </Button>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-slate-900">{estimates.length}</div>
            <p className="text-sm text-slate-600">Всего смет</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-blue-600">
              {estimates.filter(e => e.status === 'sent').length}
            </div>
            <p className="text-sm text-slate-600">Отправлено</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-600">
              {estimates.filter(e => e.status === 'approved').length}
            </div>
            <p className="text-sm text-slate-600">Одобрено</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-purple-600">
              {formatCurrency(estimates.reduce((acc, e) => acc + e.totalAmount, 0))}
            </div>
            <p className="text-sm text-slate-600">Общая сумма</p>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <Card>
          <CardContent className="p-4">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                <Input
                  placeholder="Поиск смет..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              <Select value={statusFilter} onValueChange={setStatusFilter}>
                <SelectTrigger className="w-full md:w-48">
                  <SelectValue placeholder="Статус" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Все статусы</SelectItem>
                  <SelectItem value="draft">Черновик</SelectItem>
                  <SelectItem value="sent">Отправлено</SelectItem>
                  <SelectItem value="approved">Одобрено</SelectItem>
                  <SelectItem value="rejected">Отклонено</SelectItem>
                  <SelectItem value="expired">Истекло</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Estimates Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Список смет ({filteredEstimates.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Название</TableHead>
                  <TableHead>Статус</TableHead>
                  <TableHead>Сумма</TableHead>
                  <TableHead>Действительна до</TableHead>
                  <TableHead>Создана</TableHead>
                  <TableHead>Действия</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredEstimates.map((estimate) => {
                  const StatusIcon = getStatusIcon(estimate.status);
                  const expiringSoon = estimate.validUntil && isExpiringSoon(estimate.validUntil);
                  const expired = estimate.validUntil && isExpired(estimate.validUntil);
                  
                  return (
                    <TableRow key={estimate.id}>
                      <TableCell>
                        <div className="max-w-64">
                          <div className="font-medium">{estimate.title}</div>
                          <div className="text-sm text-slate-500 truncate">
                            {estimate.description}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <StatusIcon className="h-4 w-4 text-slate-400" />
                          <Badge className={getStatusColor(estimate.status)}>
                            {getStatusBadge(estimate.status)}
                          </Badge>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="font-medium">
                          {formatCurrency(estimate.totalAmount)}
                        </div>
                        {estimate.estimateItems && estimate.estimateItems.length > 0 && (
                          <div className="text-sm text-slate-500">
                            {estimate.estimateItems.length} позиций
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        {estimate.validUntil ? (
                          <div className={`text-sm ${
                            expired ? 'text-red-600 font-medium' :
                            expiringSoon ? 'text-orange-600 font-medium' :
                            'text-slate-600'
                          }`}>
                            {formatDate(estimate.validUntil)}
                            {expired && (
                              <div className="text-xs text-red-500">Истекла</div>
                            )}
                            {expiringSoon && !expired && (
                              <div className="text-xs text-orange-500">Истекает скоро</div>
                            )}
                          </div>
                        ) : (
                          <span className="text-slate-400">Не указана</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <div className="text-sm text-slate-600">
                          {formatDate(estimate.createdAt)}
                        </div>
                        <div className="text-xs text-slate-500">
                          {estimate.user.username}
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <Button variant="ghost" size="sm">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Copy className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Download className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </motion.div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Быстрые действия</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Plus className="h-6 w-6" />
                <span className="text-sm">Новая смета</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Calculator className="h-6 w-6" />
                <span className="text-sm">Калькулятор</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <FileText className="h-6 w-6" />
                <span className="text-sm">Шаблоны</span>
              </Button>
              <Button variant="outline" className="h-24 flex flex-col items-center justify-center space-y-2">
                <Download className="h-6 w-6" />
                <span className="text-sm">Экспорт PDF</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
