
'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Plus, 
  Search, 
  Filter, 
  Download,
  Eye,
  Edit,
  Trash2,
  Phone,
  Mail,
  Calendar
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
import { 
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { formatDateTime, getStatusColor, getStatusBadge } from '@/lib/utils';
import { Lead } from '@/lib/types';

// Mock data
const mockLeads: Lead[] = [
  {
    id: '1',
    name: 'Анна Петрова',
    email: 'anna@example.com',
    phone: '+996 555 123 456',
    subject: 'Кухонная мебель',
    message: 'Интересует современная кухня для квартиры',
    status: 'new',
    score: 0.8,
    source: 'website',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 2),
    updatedAt: new Date(Date.now() - 1000 * 60 * 60),
    projects: []
  },
  {
    id: '2',
    name: 'Марат Джумабаев',
    email: 'marat@example.com',
    phone: '+996 777 987 654',
    subject: 'Мебель для офиса',
    message: 'Нужна мебель для нового офиса',
    status: 'contacted',
    score: 0.9,
    source: 'referral',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 24),
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 12),
    projects: []
  },
  {
    id: '3',
    name: 'Елена Смирнова',
    email: 'elena@example.com',
    phone: '+996 312 456 789',
    subject: 'Детская комната',
    message: 'Ищем безопасную мебель для детской',
    status: 'qualified',
    score: 0.95,
    source: 'telegram',
    createdAt: new Date(Date.now() - 1000 * 60 * 60 * 48),
    updatedAt: new Date(Date.now() - 1000 * 60 * 60 * 6),
    projects: []
  },
];

export default function CRMPage() {
  const [leads, setLeads] = useState<Lead[]>(mockLeads);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [sourceFilter, setSourceFilter] = useState('all');
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);

  const filteredLeads = leads.filter(lead => {
    const matchesSearch = lead.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         lead.subject?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || lead.status === statusFilter;
    const matchesSource = sourceFilter === 'all' || lead.source === sourceFilter;
    
    return matchesSearch && matchesStatus && matchesSource;
  });

  const getSourceBadge = (source: string) => {
    const sourceNames: Record<string, string> = {
      website: 'Сайт',
      telegram: 'Telegram',
      referral: 'Рекомендация',
      phone: 'Звонок',
      email: 'Email'
    };
    return sourceNames[source] || source;
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
          <h1 className="text-2xl font-bold text-slate-900">CRM - Управление клиентами</h1>
          <p className="text-slate-600">Управление лидами и потенциальными клиентами</p>
        </div>
        <div className="flex items-center space-x-3">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Экспорт
          </Button>
          <Button size="sm">
            <Plus className="h-4 w-4 mr-2" />
            Новый лид
          </Button>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-slate-900">{leads.length}</div>
            <p className="text-sm text-slate-600">Всего лидов</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-600">
              {leads.filter(l => l.status === 'new').length}
            </div>
            <p className="text-sm text-slate-600">Новые</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-blue-600">
              {leads.filter(l => l.status === 'qualified').length}
            </div>
            <p className="text-sm text-slate-600">Квалифицированные</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-purple-600">
              {Math.round(leads.reduce((acc, l) => acc + l.score, 0) / leads.length * 100)}%
            </div>
            <p className="text-sm text-slate-600">Средний рейтинг</p>
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
                  placeholder="Поиск по имени, email или теме..."
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
                  <SelectItem value="new">Новые</SelectItem>
                  <SelectItem value="contacted">Связались</SelectItem>
                  <SelectItem value="qualified">Квалифицированные</SelectItem>
                  <SelectItem value="converted">Конвертированные</SelectItem>
                  <SelectItem value="lost">Потерянные</SelectItem>
                </SelectContent>
              </Select>
              <Select value={sourceFilter} onValueChange={setSourceFilter}>
                <SelectTrigger className="w-full md:w-48">
                  <SelectValue placeholder="Источник" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Все источники</SelectItem>
                  <SelectItem value="website">Сайт</SelectItem>
                  <SelectItem value="telegram">Telegram</SelectItem>
                  <SelectItem value="referral">Рекомендация</SelectItem>
                  <SelectItem value="phone">Звонок</SelectItem>
                  <SelectItem value="email">Email</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Leads Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card>
          <CardHeader>
            <CardTitle>Список лидов ({filteredLeads.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Клиент</TableHead>
                  <TableHead>Контакты</TableHead>
                  <TableHead>Тема</TableHead>
                  <TableHead>Статус</TableHead>
                  <TableHead>Источник</TableHead>
                  <TableHead>Рейтинг</TableHead>
                  <TableHead>Дата создания</TableHead>
                  <TableHead>Действия</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredLeads.map((lead) => (
                  <TableRow key={lead.id}>
                    <TableCell>
                      <div>
                        <div className="font-medium">{lead.name}</div>
                        <div className="text-sm text-slate-500">{lead.email}</div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-col space-y-1">
                        {lead.phone && (
                          <div className="flex items-center text-sm">
                            <Phone className="h-3 w-3 mr-1" />
                            {lead.phone}
                          </div>
                        )}
                        <div className="flex items-center text-sm">
                          <Mail className="h-3 w-3 mr-1" />
                          {lead.email}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="max-w-48 truncate" title={lead.subject}>
                        {lead.subject}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge className={getStatusColor(lead.status)}>
                        {getStatusBadge(lead.status)}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">
                        {getSourceBadge(lead.source || '')}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-1">
                        <div className="w-16 bg-slate-200 rounded-full h-2">
                          <div 
                            className="bg-teal-500 h-2 rounded-full" 
                            style={{ width: `${lead.score * 100}%` }}
                          />
                        </div>
                        <span className="text-sm text-slate-600">
                          {Math.round(lead.score * 100)}%
                        </span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm text-slate-600">
                        {formatDateTime(lead.createdAt)}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => setSelectedLead(lead)}
                            >
                              <Eye className="h-4 w-4" />
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="max-w-2xl">
                            <DialogHeader>
                              <DialogTitle>Детали лида</DialogTitle>
                            </DialogHeader>
                            {selectedLead && (
                              <div className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                  <div>
                                    <label className="text-sm font-medium text-slate-600">Имя</label>
                                    <p className="text-slate-900">{selectedLead.name}</p>
                                  </div>
                                  <div>
                                    <label className="text-sm font-medium text-slate-600">Email</label>
                                    <p className="text-slate-900">{selectedLead.email}</p>
                                  </div>
                                  <div>
                                    <label className="text-sm font-medium text-slate-600">Телефон</label>
                                    <p className="text-slate-900">{selectedLead.phone || 'Не указан'}</p>
                                  </div>
                                  <div>
                                    <label className="text-sm font-medium text-slate-600">Статус</label>
                                    <Badge className={getStatusColor(selectedLead.status)}>
                                      {getStatusBadge(selectedLead.status)}
                                    </Badge>
                                  </div>
                                </div>
                                <div>
                                  <label className="text-sm font-medium text-slate-600">Тема</label>
                                  <p className="text-slate-900">{selectedLead.subject}</p>
                                </div>
                                <div>
                                  <label className="text-sm font-medium text-slate-600">Сообщение</label>
                                  <p className="text-slate-900">{selectedLead.message}</p>
                                </div>
                              </div>
                            )}
                          </DialogContent>
                        </Dialog>
                        <Button variant="ghost" size="sm">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="sm" className="text-red-600 hover:text-red-700">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
