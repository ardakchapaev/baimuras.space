
import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting database seeding...');

  // Create roles
  console.log('Creating roles...');
  const adminRole = await prisma.role.upsert({
    where: { name: 'admin' },
    update: {},
    create: {
      name: 'admin',
      description: 'Администратор системы',
      permissions: {
        users: ['create', 'read', 'update', 'delete'],
        projects: ['create', 'read', 'update', 'delete'],
        orders: ['create', 'read', 'update', 'delete'],
        estimates: ['create', 'read', 'update', 'delete'],
        materials: ['create', 'read', 'update', 'delete'],
        reports: ['read'],
        settings: ['read', 'update']
      }
    }
  });

  const managerRole = await prisma.role.upsert({
    where: { name: 'manager' },
    update: {},
    create: {
      name: 'manager',
      description: 'Менеджер проектов',
      permissions: {
        projects: ['create', 'read', 'update'],
        orders: ['create', 'read', 'update'],
        estimates: ['create', 'read', 'update'],
        materials: ['read'],
        reports: ['read']
      }
    }
  });

  const designerRole = await prisma.role.upsert({
    where: { name: 'designer' },
    update: {},
    create: {
      name: 'designer',
      description: 'Дизайнер мебели',
      permissions: {
        projects: ['read', 'update'],
        estimates: ['create', 'read', 'update']
      }
    }
  });

  // Create users
  console.log('Creating users...');
  const adminUser = await prisma.user.upsert({
    where: { email: 'admin@baimuras.space' },
    update: {},
    create: {
      username: 'admin',
      email: 'admin@baimuras.space',
      password_hash: await bcrypt.hash('admin123', 10),
      name: 'Администратор',
      phone: '+996 312 123 456',
      roles: {
        create: {
          roleId: adminRole.id
        }
      }
    }
  });

  const managerUser = await prisma.user.upsert({
    where: { email: 'manager@baimuras.space' },
    update: {},
    create: {
      username: 'manager',
      email: 'manager@baimuras.space',
      password_hash: await bcrypt.hash('manager123', 10),
      name: 'Марат Джумабаев',
      phone: '+996 555 987 654',
      roles: {
        create: {
          roleId: managerRole.id
        }
      }
    }
  });

  const designerUser = await prisma.user.upsert({
    where: { email: 'designer@baimuras.space' },
    update: {},
    create: {
      username: 'designer',
      email: 'designer@baimuras.space',
      password_hash: await bcrypt.hash('designer123', 10),
      name: 'Анна Петрова',
      phone: '+996 777 456 789',
      roles: {
        create: {
          roleId: designerRole.id
        }
      }
    }
  });

  // Create leads
  console.log('Creating leads...');
  const lead1 = await prisma.lead.create({
    data: {
      name: 'Анна Иванова',
      email: 'anna.ivanova@example.com',
      phone: '+996 555 123 456',
      subject: 'Кухонная мебель',
      message: 'Интересует современная кухня для квартиры',
      status: 'new',
      score: 0.8,
      source: 'website'
    }
  });

  const lead2 = await prisma.lead.create({
    data: {
      name: 'Марат Джумабаев',
      email: 'marat.djumabaev@example.com',
      phone: '+996 777 987 654',
      subject: 'Мебель для офиса',
      message: 'Нужна мебель для нового офиса',
      status: 'contacted',
      score: 0.9,
      source: 'referral'
    }
  });

  const lead3 = await prisma.lead.create({
    data: {
      name: 'Елена Смирнова',
      email: 'elena.smirnova@example.com',
      phone: '+996 312 456 789',
      subject: 'Детская комната',
      message: 'Ищем безопасную мебель для детской',
      status: 'qualified',
      score: 0.95,
      source: 'telegram'
    }
  });

  // Create projects
  console.log('Creating projects...');
  const project1 = await prisma.project.create({
    data: {
      title: 'Современная кухня для семьи Ивановых',
      description: 'Полная реконструкция кухни с современным дизайном',
      projectType: 'furniture',
      status: 'in_progress',
      budget: 450000,
      startDate: new Date('2024-01-15'),
      endDate: new Date('2024-03-01'),
      leadId: lead1.id,
      assignedUserId: managerUser.id
    }
  });

  const project2 = await prisma.project.create({
    data: {
      title: 'Детская комната Монтессори',
      description: 'Безопасная мебель для развития ребенка по методике Монтессори',
      projectType: 'furniture',
      status: 'planning',
      budget: 280000,
      startDate: new Date('2024-02-01'),
      endDate: new Date('2024-02-28'),
      leadId: lead3.id,
      assignedUserId: designerUser.id
    }
  });

  const project3 = await prisma.project.create({
    data: {
      title: 'Офисная мебель для IT-компании',
      description: 'Эргономичные рабочие места для команды разработчиков',
      projectType: 'furniture',
      status: 'completed',
      budget: 680000,
      startDate: new Date('2023-12-01'),
      endDate: new Date('2024-01-15'),
      leadId: lead2.id,
      assignedUserId: managerUser.id
    }
  });

  // Create materials
  console.log('Creating materials...');
  await prisma.material.createMany({
    data: [
      {
        name: 'Плита МДФ 18мм',
        description: 'Влагостойкая плита МДФ для мебели',
        category: 'Плиты',
        unit: 'листы',
        unitPrice: 3500,
        stockLevel: 45,
        minStock: 10,
        supplierInfo: {
          name: 'ДревПром КГ',
          contact: '+996 312 123456'
        }
      },
      {
        name: 'Фурнитура Blum',
        description: 'Петли и направляющие Blum',
        category: 'Фурнитура',
        unit: 'комплект',
        unitPrice: 8500,
        stockLevel: 3,
        minStock: 5,
        supplierInfo: {
          name: 'Мебель-Фурнитура',
          contact: '+996 555 987654'
        }
      },
      {
        name: 'Кромка ПВХ белая',
        description: 'Кромочная лента ПВХ 2мм',
        category: 'Кромки',
        unit: 'метры',
        unitPrice: 45,
        stockLevel: 850,
        minStock: 100,
        supplierInfo: {
          name: 'Техно-Кромка',
          contact: '+996 777 456789'
        }
      },
      {
        name: 'Лак полиуретановый',
        description: 'Защитный лак для древесины',
        category: 'Химия',
        unit: 'литры',
        unitPrice: 1200,
        stockLevel: 12,
        minStock: 5,
        supplierInfo: {
          name: 'ХимПром',
          contact: '+996 312 789012'
        }
      }
    ]
  });

  // Create orders
  console.log('Creating orders...');
  const order1 = await prisma.order.create({
    data: {
      orderNumber: 'BM240001',
      title: 'Кухонный гарнитур "Модерн"',
      description: 'Полный кухонный гарнитур с островом',
      status: 'in_production',
      totalAmount: 450000,
      paidAmount: 225000,
      discount: 0,
      deliveryDate: new Date('2024-02-15'),
      installationDate: new Date('2024-02-16'),
      projectId: project1.id,
      assignedUserId: managerUser.id
    }
  });

  const order2 = await prisma.order.create({
    data: {
      orderNumber: 'BM240002',
      title: 'Детская мебель Монтессори',
      description: 'Кровать, стол, стеллажи для детской',
      status: 'confirmed',
      totalAmount: 180000,
      paidAmount: 54000,
      discount: 10000,
      deliveryDate: new Date('2024-02-20'),
      projectId: project2.id,
      assignedUserId: designerUser.id
    }
  });

  // Create estimates
  console.log('Creating estimates...');
  await prisma.estimate.create({
    data: {
      title: 'Кухонный гарнитур для квартиры',
      description: 'Современная кухня с островом, техника встроенная',
      totalAmount: 450000,
      validUntil: new Date('2024-02-28'),
      status: 'sent',
      notes: 'Включена установка и доставка',
      projectId: project1.id,
      userId: managerUser.id,
      estimateItems: {
        create: [
          {
            description: 'Кухонные шкафы верхние',
            quantity: 8,
            unitPrice: 25000,
            totalPrice: 200000
          },
          {
            description: 'Кухонные шкафы нижние',
            quantity: 6,
            unitPrice: 30000,
            totalPrice: 180000
          },
          {
            description: 'Столешница из кварца',
            quantity: 1,
            unitPrice: 70000,
            totalPrice: 70000
          }
        ]
      }
    }
  });

  // Create measurements
  console.log('Creating measurements...');
  await prisma.measurement.createMany({
    data: [
      {
        title: 'Замер кухни у Ивановых',
        description: 'Замер для кухонного гарнитура',
        scheduledAt: new Date('2024-02-05T10:00:00'),
        duration: 90,
        status: 'scheduled',
        address: 'ул. Московская, 123, кв. 45',
        notes: 'Перезвонить за день до визита',
        projectId: project1.id,
        userId: managerUser.id
      },
      {
        title: 'Замер детской комнаты',
        description: 'Мебель Монтессори для ребенка',
        scheduledAt: new Date('2024-02-05T14:00:00'),
        duration: 60,
        status: 'scheduled',
        address: 'пр. Манаса, 67, кв. 12',
        notes: 'Есть домофон, код 1234',
        projectId: project2.id,
        userId: designerUser.id
      }
    ]
  });

  // Create payments
  console.log('Creating payments...');
  await prisma.payment.createMany({
    data: [
      {
        orderId: order1.id,
        amount: 225000,
        paymentMethod: 'bank_transfer',
        status: 'completed',
        transactionId: 'TXN001',
        paidAt: new Date('2024-01-20T15:30:00')
      },
      {
        orderId: order2.id,
        amount: 54000,
        paymentMethod: 'cash',
        status: 'completed',
        paidAt: new Date('2024-01-25T11:00:00')
      }
    ]
  });

  console.log('✅ Database seeding completed successfully!');
  console.log('');
  console.log('Demo credentials:');
  console.log('Admin: admin@baimuras.space / admin123');
  console.log('Manager: manager@baimuras.space / manager123');
  console.log('Designer: designer@baimuras.space / designer123');
}

main()
  .catch((e) => {
    console.error('❌ Error seeding database:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
